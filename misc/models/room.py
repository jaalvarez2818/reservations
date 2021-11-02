from django.db import models

from misc.models import RoomTypology, Active
from misc.utils import words


class Room(Active):
    number = models.PositiveSmallIntegerField(verbose_name=words.NUMBER)
    room_typology = models.ForeignKey(RoomTypology, verbose_name=words.ROOM_TYPOLOGY, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'misc_room'
        verbose_name = words.ROOM
        verbose_name_plural = words.ROOMS

    def __str__(self):
        return str(self.number)
