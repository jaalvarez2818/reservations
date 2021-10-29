import base64
import io

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import get_language
from phonenumber_field.modelfields import PhoneNumberField

from misc.models import RoomTypology, Room
from misc.utils import words

STATUS = (
    ('pendent', words.PENDENT),
    ('approved', words.APPROVED),
    ('rejected', words.REJECTED),
    ('executed', words.EXECUTED),
    ('not_executed', words.NOT_EXECUTED),
)


class Reservation(models.Model):
    start_date = models.DateField(verbose_name=words.START_DATE)
    end_date = models.DateField(verbose_name=words.END_DATE)
    room_typology = models.ForeignKey(RoomTypology, verbose_name=words.ROOM_TYPOLOGY, on_delete=models.CASCADE)
    guests = models.PositiveSmallIntegerField(verbose_name=words.GUESTS)
    name = models.CharField(max_length=100, verbose_name=words.NAME)
    email = models.EmailField(verbose_name=words.EMAIL)
    phone = PhoneNumberField(verbose_name=words.PHONE)
    price = models.FloatField(verbose_name=words.PRICE)
    locator = models.CharField(max_length=16, verbose_name=words.LOCATOR, unique=True)
    room = models.ForeignKey(Room, verbose_name=words.ROOM, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=words.DATETIME)
    status = models.CharField(max_length=12, verbose_name=words.STATUS, choices=STATUS)

    class Meta:
        db_table = 'misc_reservation'
        verbose_name = words.RESERVATION
        verbose_name_plural = words.RESERVATIONS
        ordering = ('start_date',)

    def save(self, **kwargs):
        if self.pk is None:
            current = now()
            date = format(current, '%Y%m%d')
            count = Reservation.objects.filter(datetime__date=current.date()).count()
            number = str(count + 1).rjust(3, '0')
            self.locator = f'RES-{date}-{number}'
        super().save(**kwargs)

    def status_color(self):
        return {
            'pendent': 'warning',
            'approved': 'primary',
            'rejected': 'danger',
            'executed': 'success',
            'not_executed': 'dark'
        }[self.status]

    def status_flow(self):
        return {
            'pendent': [
                {
                    'text': words.APPROVE,
                    'url': reverse('reservation_approve', kwargs={'pk': self.pk}),
                    'icon': 'la la-check'
                },
                {
                    'text': words.REJECT,
                    'url': reverse('reservation_reject', kwargs={'pk': self.pk}),
                    'icon': 'la la-ban'
                }
            ],
            'approved': [
                {
                    'text': words.EXECUTE,
                    'url': reverse('reservation_execute', kwargs={'pk': self.pk}),
                    'icon': 'la la-check'
                },
                {
                    'text': words.NOT_EXECUTE,
                    'url': reverse('reservation_not_execute', kwargs={'pk': self.pk}),
                    'icon': 'la la-ban'
                }
            ],
            'rejected': [],
            'executed': [],
            'not_executed': []
        }[self.status]

    def __str__(self):
        return self.locator

    def days(self):
        return (self.end_date - self.start_date).days

    def get_qr(self):
        import qrcode

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f'{settings.SERVER_URL}/{get_language()}/details/{self.locator}')
        qr.make(fit=True)

        image = qr.make_image(fill_color="black", back_color="white")
        in_mem_file = io.BytesIO()
        image.save(in_mem_file, format="PNG")
        in_mem_file.seek(0)
        img_bytes = in_mem_file.read()
        base64_encoded_result_bytes = base64.b64encode(img_bytes)
        base64_encoded_result_str = base64_encoded_result_bytes.decode('ascii')
        return base64_encoded_result_str
