from __future__ import unicode_literals


from django.contrib.auth.models import AbstractUser, Group, UserManager

from accounts.my_fields import UserRoleField


class CustomUserManager(UserManager):
    def create_user(self, *args, **kwargs):
        user = UserManager.create_user(self, *args, **kwargs)

        group_name = 'teachers' if user.role == 'TE' else 'students'
        group = Group.objects.get(name=group_name)
        if group is not None:
            group.user_set.add(user)

        return user


class User(AbstractUser):
    role = UserRoleField(
        default='ST',
        blank=False,
        help_text='Role of the user can be ST (Student) or TE (Teacher)'
    )

    objects = CustomUserManager()
