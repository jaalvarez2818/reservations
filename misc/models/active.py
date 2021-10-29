from django.db import models

from misc.utils import words


class Active(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=words.IS_ACTIVE)

    class Meta:
        abstract = True

    def delete(self, **kwargs):
        self.is_active = False
        self.save()
