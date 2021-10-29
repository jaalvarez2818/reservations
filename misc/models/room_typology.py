from django.db import models

from misc.models import Active
from misc.utils import words


class RoomTypology(Active):
    name = models.CharField(max_length=50, verbose_name=words.NAME)
    max_people = models.PositiveSmallIntegerField(verbose_name=words.MAX_PEOPLE)
    price = models.FloatField(verbose_name=words.PRICE)

    class Meta:
        db_table = 'misc_room_typology'
        verbose_name = words.ROOM_TYPOLOGY
        verbose_name_plural = words.ROOM_TYPOLOGIES

    def __str__(self):
        return self.name
