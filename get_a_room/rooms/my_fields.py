from django.db import models


DAYS_OF_THE_WEEK = (
    ('MO', 'Monday'),
    ('TU', 'Tuesday'),
    ('WE', 'Wednesday'),
    ('TH', 'Thursday'),
    ('FR', 'Friday'),
    ('SA', 'Saturday'),
    ('SU', 'Sunday'),
)


class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = DAYS_OF_THE_WEEK
        kwargs['max_length'] = 2
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)
