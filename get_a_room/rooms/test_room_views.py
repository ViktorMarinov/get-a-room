from rooms.models import Room
from accounts.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from django.core.urlresolvers import reverse


class RoomViewTests(APITestCase):

    ROOM_COUNT = 1

    ROOM_NUMBER = 320

    ROOM_CAPACITY = 20

    ROOMS_LIST_PATH = reverse('room-list')

    ROOM_DETAILS_PATH = reverse('room-detail', args=[ROOM_NUMBER])

    FILTER_PATH = ROOMS_LIST_PATH + 'filter/'

    def setUp(self):
        self.user = User.objects.get(username='admin')
        self.client.force_authenticate(user=self.user)

        Room.create(self.ROOM_NUMBER, self.ROOM_CAPACITY, True)

    def test_get_list(self):
        response = self.client.get(self.ROOMS_LIST_PATH)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['count'], self.ROOM_COUNT)

    def test_get_details(self):
        response = self.client.get(self.ROOM_DETAILS_PATH)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_data['capacity'], self.ROOM_CAPACITY,
            msg='Capacity of new room should be {} but it is {}'.format(
                self.ROOM_CAPACITY, response_data['capacity'])
        )
        self.assertTrue(response_data['is_computer_room'])

    def test_room_post(self):
        data = {
            "number": "101",
            "capacity": 100,
            "is_computer_room": False
        }
        response = self.client.post(self.ROOMS_LIST_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            room = Room.objects.get(number=101)
            self.assertEqual(room.capacity, 100)
            self.assertFalse(room.is_computer_room)
        except:
            self.fail(msg='Getting the new room failed!')

    def test_room_put(self):
        data = {
            "number": self.ROOM_NUMBER,
            "capacity": self.ROOM_CAPACITY + 10
        }
        response = self.client.put(self.ROOM_DETAILS_PATH, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        try:
            room = Room.objects.get(number=self.ROOM_NUMBER)
            self.assertEqual(room.capacity, self.ROOM_CAPACITY + 10)
        except:
            self.fail(msg='Getting room with number {} failed'.format(
                self.ROOM_NUMBER)
            )

    def test_filter(self):
        Room.create(325, 100, False)
        Room.create(314, 20, True)

        response = self.client.get(self.FILTER_PATH,
                                   data={'is_computer_room': 'true'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        for dict_ in response_data:
            self.assertTrue(dict_['is_computer_room'])

    def test_filter_min_capacity(self):
        Room.create(326, 100, False)
        Room.create(315, 20, True)

        response = self.client.get(self.FILTER_PATH,
                                   data={'min_capacity': 50})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        for dict_ in response_data:
            self.assertGreaterEqual(dict_['capacity'], 50)
