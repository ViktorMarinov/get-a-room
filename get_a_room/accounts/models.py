from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from accounts.my_fields import UserRoleField

class User(AbstractUser):
    role = UserRoleField(
        default='ST',
        blank=False,
        help_text='Role of the user can be ST (Student) or TE (Teacher)'
    )
