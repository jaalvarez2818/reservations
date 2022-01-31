from datetime import datetime
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from misc.models import Reservation, RoomTypology, UnpleasantCustomer
from misc.models.reservation import STATUS
from misc.utils import words
from misc.utils.pdf import export_pdf_from_html


class ReservationListView(ListView):
    template_name = 'reservation/list.html'
    model = Reservation
    paginate_by = 15

    def get_queryset(self):
        filters = {}
        status = self.request.GET.get('status')
        room_typology = self.request.GET.get('room_typology')
        if status:
            filters.update({'status': status})
        if room_typology:
            filters.update({'room_typology': room_typology})
        queryset = super().get_queryset()
        if filters:
            queryset = queryset.filter(**filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.RESERVATIONS.capitalize(),
            'content_title': words.RESERVATIONS.capitalize(),
            'content_subtitle': words.LIST.capitalize(),
            'statuses': STATUS,
            'room_typologies': RoomTypology.objects.filter(is_active=True)
        })
        return context


class ReservationApproveView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Reservation, pk=self.kwargs.get('pk'), status='pendent')
        obj.status = 'approved'
        obj.save()
        messages.success(request, words.RESERVATION_APPROVED.capitalize())
        return redirect(reverse('reservation_list'))


class ReservationRejectView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Reservation, pk=self.kwargs.get('pk'), status='pendent')
        obj.status = 'rejected'
        obj.save()
        messages.success(request, words.RESERVATION_REJECTED.capitalize())
        return redirect(reverse('reservation_list'))


class ReservationExecuteView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Reservation, pk=self.kwargs.get('pk'), status='approved')
        obj.status = 'executed'
        obj.save()
        messages.success(request, words.RESERVATION_EXECUTED.capitalize())
        return redirect(reverse('reservation_list'))


class ReservationNotExecuteView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(Reservation, pk=self.kwargs.get('pk'), status='approved')
        obj.status = 'not_executed'
        obj.save()
        messages.success(request, words.RESERVATION_NOT_EXECUTED.capitalize())
        return redirect(reverse('reservation_list'))


class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservation/details.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Reservation, locator=self.kwargs.get('locator'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': f'{words.RESERVATION.capitalize()} {self.object.locator}'
        })
        return context


class ReservationPDFView(DetailView):
    template_name = 'reservation/pdf.html'
    model = Reservation

    def get(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, locator=self.kwargs.get('locator'))
        options = {
            'page-height': '27.94cm',
            'page-width': '22cm',
            'margin-top': '1cm',
            'margin-right': '1cm',
            'margin-bottom': '1cm',
            'margin-left': '1cm',
            'encoding': "UTF-8",
            'no-outline': None
        }
        data = {'reservation': reservation}
        pdf = export_pdf_from_html(request, f'{words.RESERVATION.capitalize()} {reservation.locator}',
                                   self.template_name, options, data)
        return pdf


class LocatorView(TemplateView):
    template_name = 'reservation/locator.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.LOCATOR.capitalize(),
            'found': None
        })
        return context

    def post(self, request, *args, **kwargs):
        locator = request.POST.get('locator')

        try:
            reservation = Reservation.objects.get(locator=locator.upper())
            found = True
        except Reservation.DoesNotExist:
            found = False

        title = words.LOCATOR.capitalize()
        return render(request, self.template_name, locals())


class StatisticsView(TemplateView):
    template_name = 'reservation/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        total = Reservation.objects.count()

        context.update({
            'title': words.STATISTICS.capitalize(),
            'total_amount': Reservation.objects.filter(status='executed').aggregate(total_amount=Sum('price'))[
                                'total_amount'] or 0,
            'by_status': {
                status[1]: {
                    'color': {
                        'pendent': 'warning',
                        'approved': 'primary',
                        'rejected': 'danger',
                        'executed': 'success',
                        'not_executed': 'dark'
                    }[status[0]],
                    'percent': str(Reservation.objects.filter(status=status[0]).count() * 100 / total)
                }
                for status in STATUS
            }
        })
        return context


class ReservationCreateView(View):
    def get(self, request, *args, **kwargs):
        title = words.CREATE_RESERVATION.capitalize()
        room_typologies = RoomTypology.objects.filter(is_active=True)
        return render(request, 'reservation/create.html', locals())

    def post(self, request, *args, **kwargs):
        if request.is_ajax():

            dates = request.POST.get('dates').split(' - ')
            start = datetime.strptime(dates[0], '%m/%d/%Y')
            end = datetime.strptime(dates[1], '%m/%d/%Y')

            if start.date() < timezone.now().date():
                return JsonResponse(safe=False,
                                    data={'error': True, 'message': words.START_DATE_GREATER_THAN_CURRENT.capitalize()})

            if UnpleasantCustomer.objects.filter(email=request.POST.get('email'), is_active=True).exists():
                return JsonResponse(safe=False,
                                    data={'error': True, 'message': words.YOU_NOT_RESERVATIONS.capitalize()})

            try:
                room_typology = RoomTypology.objects.get(pk=request.POST.get('room_typology'), is_active=True)

                count = Reservation.objects.filter(
                    Q(start_date__lte=start, end_date__gte=start) | Q(start_date__lte=end, end_date__gte=end) | Q(
                        start_date__gte=start, end_date__lte=end), room_typology_id=room_typology).exclude(
                    status__in=['rejected', 'not_executed']).count()

                if count >= room_typology.qty:
                    return JsonResponse(safe=False,
                                        data={'error': True, 'message': words.NOT_AVAILABILITY.capitalize()})

                Reservation.objects.create(
                    start_date=start.date(),
                    end_date=end.date(),
                    room_typology=room_typology,
                    guests=request.POST.get('guests'),
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    phone=request.POST.get('phone'),
                    price=room_typology.price * int(request.POST.get('guests')),
                    status='pendent'
                )

                messages.success(request, words.RESERVATION_CREATED.capitalize())

                return JsonResponse(
                    safe=False,
                    data={'error': False, 'redirect_to': reverse('reservation_list')}
                )

            except RoomTypology.DoesNotExist:
                return JsonResponse(safe=False, data={'error': True, 'message': words.TYPOLOGY_NOT_EXISTS.capitalize()})

        return JsonResponse(
            safe=False,
            data={'error': True, 'message': words.INVALID_REQUEST.capitalize()}
        )


class CheckAvailabilityView(View):
    def get(self, request, *args, **kwargs):
        room_typology = request.GET.get('room_typology')
        start = datetime.strptime(request.GET.get('start_date'), '%m/%d/%Y')
        end = datetime.strptime(request.GET.get('end_date'), '%m/%d/%Y')

        if start.date() < timezone.now().date():
            return JsonResponse(safe=False,
                                data={'error': True, 'message': words.START_DATE_GREATER_THAN_CURRENT.capitalize()})

        try:
            room_typology = RoomTypology.objects.get(pk=room_typology, is_active=True)

            count = Reservation.objects.filter(
                Q(start_date__lte=start, end_date__gte=start) | Q(start_date__lte=end, end_date__gte=end) | Q(
                    start_date__gte=start, end_date__lte=end), room_typology_id=room_typology).exclude(
                status__in=['rejected', 'not_executed']).count()

            if count < room_typology.qty:
                return JsonResponse(safe=False, data={'availability': True, 'max': room_typology.max_people})
            return JsonResponse(safe=False,
                                data={'availability': False, 'message': words.NOT_AVAILABILITY.capitalize()})

        except RoomTypology.DoesNotExist:
            return JsonResponse(safe=False, data={'error': True, 'message': words.TYPOLOGY_NOT_EXISTS.capitalize()})


class CheckPersonView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')

        if UnpleasantCustomer.objects.filter(email=email, is_active=True).exists():
            return JsonResponse(safe=False,
                                data={'can_reservate': False, 'message': words.YOU_NOT_RESERVATIONS.capitalize()})
        return JsonResponse(safe=False, data={'can_reservate': True})
