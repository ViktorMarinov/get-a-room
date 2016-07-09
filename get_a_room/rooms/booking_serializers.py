from accounts.views import UserViewSet

from rooms.models import Booking
from rooms.room_views import RoomViewSet

from rest_framework import serializers


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model, used to represent the model 
    to the API and vice versa
    """

    room_number = serializers.PrimaryKeyRelatedField(
        queryset=RoomViewSet.queryset
    )

    user = serializers.SlugRelatedField(
        queryset=UserViewSet.queryset,
        allow_null=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def update(self, *args, **kwargs):
        old_booking = args[0]
        new_data = args[1]
        old_booking.check_time_slot(new_data)
        return super(BookingSerializer, self).update(*args, **kwargs)

    def validate(self, data):
        super(BookingSerializer, self).validate(data)
        booking = Booking(**data)
        booking.clean()
        return data

    class Meta:
        model = Booking
        fields = (
            'url',
            'room_number',
            'user',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'day_of_week'
        )
