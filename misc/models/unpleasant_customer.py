from django.db import models

from misc.models import Active
from misc.utils import words


class UnpleasantCustomer(Active):
    email = models.EmailField(verbose_name=words.EMAIL, unique=True)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=words.DATETIME)
    reason = models.TextField(verbose_name=words.REASON)

    class Meta:
        db_table = 'misc_unpleasant_customer'
        verbose_name = words.UNPLEASANT_CUSTOMER
        verbose_name_plural = words.UNPLEASANT_CUSTOMERS
        ordering = ('email',)

    def __str__(self):
        return str(self.email)
