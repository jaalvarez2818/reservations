from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView

from misc.forms import UnpleasantCustomerForm
from misc.models import UnpleasantCustomer
from misc.utils import words


class UnpleasantCustomerListView(ListView):
    template_name = 'unpleasant_customer/list.html'
    model = UnpleasantCustomer
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.UNPLEASANT_CUSTOMERS.capitalize(),
            'content_title': words.UNPLEASANT_CUSTOMERS.capitalize(),
            'content_subtitle': words.LIST.capitalize()
        })
        return context


class UnpleasantCustomerActiveView(View):
    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(UnpleasantCustomer, pk=self.kwargs.get('pk'))
        obj.is_active = not obj.is_active
        obj.save()
        if obj.is_active:
            messages.success(request, words.UNPLEASANT_CUSTOMER_ENABLED.capitalize())
        else:
            messages.success(request, words.UNPLEASANT_CUSTOMER_DISABLED.capitalize())
        return redirect(reverse('unpleasant_customer_list'))


class UnpleasantCustomerCreateView(CreateView, SuccessMessageMixin):
    template_name = 'unpleasant_customer/form.html'
    model = UnpleasantCustomer
    form_class = UnpleasantCustomerForm
    success_url = reverse_lazy('unpleasant_customer_list')
    success_message = words.UNPLEASANT_CUSTOMER_CREATED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.CREATE_UNPLEASANT_CUSTOMER.capitalize(),
            'content_title': words.CREATE_UNPLEASANT_CUSTOMER.capitalize(),
            'action': 'create'
        })
        return context


class UnpleasantCustomerUpdateView(UpdateView, SuccessMessageMixin):
    template_name = 'unpleasant_customer/form.html'
    model = UnpleasantCustomer
    form_class = UnpleasantCustomerForm
    success_url = reverse_lazy('unpleasant_customer_list')
    success_message = words.UNPLEASANT_CUSTOMER_UPDATED

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': words.UPDATE_UNPLEASANT_CUSTOMER.capitalize(),
            'content_title': words.UPDATE_UNPLEASANT_CUSTOMER.capitalize(),
            'action': 'update'
        })
        return context
