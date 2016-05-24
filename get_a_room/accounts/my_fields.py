from django.db import models


USER_ROLES = (
    ('ST', 'Student'),
    ('TE', 'Teacher')
)


class UserRoleField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['default'] = 'ST'
        kwargs['max_length'] = 2
        kwargs['choices'] = USER_ROLES
        super(UserRoleField, self).__init__(*args, **kwargs)
