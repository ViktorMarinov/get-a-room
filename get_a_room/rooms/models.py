from __future__ import unicode_literals
import datetime

from rooms import my_fields

from django.db import models
from django.conf import settings

from rest_framework import serializers


class Room(models.Model):
    """
    A model representing a room of the faculty
    """
    number = models.IntegerField(primary_key=True, unique=True, blank=False)
    capacity = models.PositiveIntegerField(blank=False)
    is_computer_room = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

    @classmethod
    def create(cls, number, capacity, is_computer_room):
        room = cls(number=number,
                   capacity=capacity,
                   is_computer_room=is_computer_room)
        room.save()
        return room


class BookingManager(models.Manager):
    def create(*args, **kwargs):
        Booking.check_time_slot(None, kwargs)
        return models.Manager.create(*args, **kwargs)


class Booking(models.Model):
    """
    A model representing a single booking.
    It may book only one day per week in the period
    start date to end date in the time interval
    start time to end time
    """
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
        """
        Checks if the values of a new booking are valid
        """
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

    def check_time_slot(self, new_data):
        """
        Checks if the time slot in new_data is available.
        If a booking is getting updated then it is skipped
        when checking the availability of the room.
        """
        bookings_on_room = Booking.objects.filter(
            room_number=new_data['room_number'])
        id = None
        if self is not None:
            id = self.id
        for booking in bookings_on_room:
            if id is not None and id == booking.id:
                continue

            if booking.day_of_week == new_data['day_of_week']:
                if (booking.end_date >= new_data['start_date'] and
                   booking.start_date <= new_data['end_date']):
                    if (booking.end_time > new_data['start_time'] and
                       booking.start_time < new_data['end_time']):
                        raise serializers.ValidationError(
                            "Time slot is not available for that room")

    def __str__(self):
        return "{} {} Dates: {} - {} Time: {} - {} Day: {}".format(
            self.room_number, self.user, self.start_date, self.end_date,
            self.start_time, self.end_time, self.day_of_week)
