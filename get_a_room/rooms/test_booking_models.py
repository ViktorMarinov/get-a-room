from datetime import date, time

from accounts.models import User
from rooms.models import Booking, Room

from django.test import TestCase

from rest_framework.exceptions import ValidationError


class BookingModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.room = Room.objects.create(number=100, capacity=20)

    def test_create_booking(self):
        Booking.objects.create(
            user=self.user, room_number=self.room,
            start_date=date(2016, 7, 22), end_date=date(2016, 7, 29),
            start_time=time(1, 0), end_time=time(2, 0),
            day_of_week='MO'
        )
        self.assertIsNotNone(Booking.objects.get(
            room_number=self.room))

    def test_create_overlaping_booking_should_fail(self):
        self.test_create_booking()
        self.assertRaises(
            ValidationError,
            Booking.objects.create,
            user=self.user, room_number=self.room,
            start_date=date(2016, 7, 22), end_date=date(2016, 7, 29),
            start_time=time(1, 30), end_time=time(3, 0),
            day_of_week='MO'
        )

    def test_invalid_dates_should_raise(self):
        booking = Booking.objects.create(
            user=self.user, room_number=self.room,
            start_date=date(2016, 7, 30), end_date=date(2016, 7, 29),
            start_time=time(1, 0), end_time=time(2, 0),
            day_of_week='MO'
        )
        self.assertRaises(
            ValidationError,
            booking.clean
        )
