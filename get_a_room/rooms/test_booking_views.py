from datetime import date, time

from rooms.models import Booking, Room
from accounts.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from django.core.urlresolvers import reverse


class BookingViewTests(APITestCase):

    BOOKING_ROOM_NUMBER = 101

    BOOKINGS_LIST_PATH = reverse('booking-list')

    FILTER_PATH = BOOKINGS_LIST_PATH + 'filter/'

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.room = Room.objects.create(
            number=self.BOOKING_ROOM_NUMBER, capacity=20)
        self.test_booking = Booking.objects.create(
            user=self.user, room_number=self.room,
            start_date=date(2016, 7, 22), end_date=date(2016, 7, 29),
            start_time=time(1, 0), end_time=time(2, 0),
            day_of_week='MO'
        )
        self.booking_id = self.test_booking.id
        self.client.force_authenticate(user=self.user)

    def test_get_list(self):
        response = self.client.get(self.BOOKINGS_LIST_PATH)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['count'], 1)

    def test_get_details(self):
        response = self.client.get(
            self.BOOKINGS_LIST_PATH + str(self.booking_id) + '/')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for key in response_data:
            if key == 'url':
                continue
            self.assertEqual(
                str(response_data[key]), str(getattr(self.test_booking, key)),
                msg='{} is not {}'.format(
                    response_data[key], getattr(self.test_booking, key)
                )
            )

    def test_booking_post(self):
        data = {
            "user": self.user.username,
            "room_number": self.room.number,
            "start_date": "2016-07-15",
            "end_date": "2016-07-19",
            "start_time": "01:00:00",
            "end_time": "02:00:00",
            "day_of_week": "MO"
        }
        response = self.client.post(self.BOOKINGS_LIST_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            Booking.objects.get(
                user=self.user, start_date=date(2016, 7, 15))
        except Exception as e:
            self.fail(msg='Getting the new booking failed' + e)

    def test_booking_put(self):
        data = {
            "start_date": "2016-08-15",
            "end_date": "2016-08-19",
            "start_time": "01:00:00",
            "end_time": "02:00:00",
            "day_of_week": "MO"
        }
        details_path = self.BOOKINGS_LIST_PATH + str(self.booking_id) + '/'
        response = self.client.put(details_path, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            Booking.objects.get(
                user=self.user, start_date=date(2016, 8, 15))
        except Exception as e:
            self.fail(msg='Getting the new booking failed' + e)
