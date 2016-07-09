from accounts.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from django.core.urlresolvers import reverse


class UserViewTests(APITestCase):

    USER_LIST_PATH = reverse('user-list')

    FILTER_PATH = USER_LIST_PATH + 'filter/'

    REGISTER_PATH = '/accounts/register/'

    def setUp(self):
        self.user = User.objects.get(username='admin')

    def test_authentication_fail(self):
        response = self.client.get(self.USER_LIST_PATH)
        self.assertEqual(response.status_code, 403)

    def test_authentication_success(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.USER_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_username(self):
        User.objects.create_user(username='anotherUser')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.FILTER_PATH,
                                   data={'username': 'admin'})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg="Filtering by username status code is not 200")
        self.assertEqual(response.json()[0]['username'], 'admin')

    def test_filter_by_role(self):
        User.objects.create_user(username='s1', role='ST')
        User.objects.create_user(username='s2', role='ST')
        User.objects.create_user(username='t1', role='TE')

        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.FILTER_PATH, data={'role': 'ST'})
        self.assertEqual(
            response.status_code, status.HTTP_200_OK,
            msg="Filtering by role status code is not 200")
        for dict_ in response.json():
            self.assertEqual(dict_['role'], 'ST')

    def test_register(self):
        expected_mail = 'newuser@fakemail.com'
        username = 'new_user'
        password = 'hardpass'
        data = {'username': username,
                'password': password,
                'role': 'TE',
                'email': expected_mail}
        response = self.client.post(self.REGISTER_PATH, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        try:
            user = User.objects.get(username=username)
            self.assertEqual(
                user.role, 'TE',
                msg='Role should be {} but it is {}'.format(
                    'TE', user.role))
            self.assertEqual(
                user.email, expected_mail,
                msg='Email should be {} but it is {}'.format(
                    expected_mail, user.email))
            self.assertTrue(
                self.client.login(username=username, password=password),
                msg='The user could not login.')
        except:
            self.fail(msg='Getting the new user failed')
