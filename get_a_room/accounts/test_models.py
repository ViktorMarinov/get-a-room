from accounts.models import User

from django.test import TestCase


class UserTests(TestCase):

    def test_create_user(self):
        User.objects.create_user(username='test1', password='test1')
        self.assertIsNotNone(User.objects.get(username='test1'))

    def test_adding_user_to_student_group(self):
        user = User.objects.create_user(
            username='FakeUser',
            password='EasyPass',
            role='ST'
        )
        groups_names = user.groups.values_list('name', flat=True)
        self.assertIn(
            'students', groups_names,
            msg="User with role ST not added to students group!"
        )

    def test_adding_user_to_teachers_group(self):
        user = User.objects.create_user(
            username='FakeUser',
            password='EasyPass',
            role='TE'
        )
        groups_names = user.groups.values_list('name', flat=True)
        self.assertIn(
            'teachers', groups_names,
            msg="User with role ST not added to teachers group!"
        )
