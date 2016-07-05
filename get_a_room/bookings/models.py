from __future__ import unicode_literals
import datetime

from django.db import models
from django.conf import settings

from rest_framework import serializers

from bookings import my_fields
from rooms.models import Room


class BookingManager(models.Manager):
    def create(*args, **kwargs):
        booking_on_room = Booking.objects.filter(
            room_number=kwargs['room_number'])
        for booking in booking_on_room:
            if booking.day_of_week == kwargs['day_of_week']:
                if (booking.end_date >= kwargs['start_date'] and
                   booking.start_date <= kwargs['end_date']):
                    if (booking.end_time > kwargs['start_time'] and
                       booking.start_time < kwargs['end_time']):
                        raise serializers.ValidationError(
                            "Time slot is not available for that room")

        return models.Manager.create(*args, **kwargs)


class Booking(models.Model):
    room_number = models.ForeignKey(
        Room,
        related_name='booking',
        on_delete=models.CASCADE,
        blank=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='booking',
        on_delete=models.CASCADE,
        blank=False
    )
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(blank=False)
    end_time = models.TimeField(blank=False)
    day_of_week = my_fields.DayOfTheWeekField()

    objects = BookingManager()

    def clean(self):
        if self.start_date > self.end_date:
            raise serializers.ValidationError(
                "Start date cannot be after end date!")

        if self.start_date < datetime.datetime.now().date():
            raise serializers.ValidationError(
                "Start date cannot be in the past!")

        if self.start_time > self.end_time:
            raise serializers.ValidationError(
                "Start time cannot be after end time!")

        if self.start_date == self.end_date:
            start_day_of_week = self.start_date.weekday()
            day_name = my_fields.DAYS_OF_THE_WEEK[start_day_of_week]
            if day_name[0] != self.day_of_week:
                raise serializers.ValidationError(
                    "Day of week does not match given dates")

        else:
            flag = False
            date_iter = self.start_date
            max_iter_date = self.start_date + datetime.timedelta(6)
            while date_iter <= self.end_date and date_iter <= max_iter_date:
                day = my_fields.DAYS_OF_THE_WEEK[date_iter.weekday()]
                if day[0] == self.day_of_week:
                    flag = True
                    break
                date_iter = date_iter + datetime.timedelta(1)
            if not flag:
                raise serializers.ValidationError(
                    "Day of week does not match given dates")

    def __str__(self):
        return "{} {} Dates: {} - {} Time: {} - {} Day: {}".format(
            self.room_number, self.user, self.start_date, self.end_date,
            self.start_time, self.end_time, self.day_of_week)
