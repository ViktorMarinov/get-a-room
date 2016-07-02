from django.db import models

# Create your models here.


class Room(models.Model):
    number = models.IntegerField(primary_key=True, unique=True, blank=False)
    capacity = models.PositiveIntegerField(blank=False)
    is_computer_room = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

    @classmethod
    def create(cls, number, capacity, is_computer_room):
        room = cls(number=number,
                   capacity=capacity,
                   is_computer_room=is_computer_room)
        return room
