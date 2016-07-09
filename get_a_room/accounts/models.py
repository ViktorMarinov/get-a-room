from __future__ import unicode_literals


from django.contrib.auth.models import AbstractUser, Group, UserManager

from accounts.my_fields import UserRoleField


class CustomUserManager(UserManager):
    """
    Manager for User objects, automaticly adding the users
    in teachers or students group, depending on their role
    """
    def create_user(self, *args, **kwargs):
        user = UserManager.create_user(self, *args, **kwargs)

        group_name = 'teachers' if user.role == 'TE' else 'students'
        group = Group.objects.get(name=group_name)
        if group is not None:
            group.user_set.add(user)

        return user


class User(AbstractUser):
    """
    A model representing a user. Extends the AbstractUser
    with a role field, used to determine if the user is
    teacher or student
    """
    role = UserRoleField(
        default='ST',
        blank=False,
        help_text='Role of the user can be ST (Student) or TE (Teacher)'
    )

    objects = CustomUserManager()
