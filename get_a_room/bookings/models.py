from __future__ import unicode_literals
from django.db import models
from django.conf import settings

from bookings import my_fields
from rooms.models import Room


# Create your models here.

class Booking(models.Model):
    room_number = models.ForeignKey(
        Room,
        related_name='booking',
        on_delete=models.CASCADE
    )
    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='booking',
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = my_fields.DayOfTheWeekField()

    def __str__(self):
        return str(self.__dict__)
