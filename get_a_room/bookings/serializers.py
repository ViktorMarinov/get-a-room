from rest_framework import serializers

from bookings.models import Booking

from accounts.views import UserViewSet

from rooms.views import RoomViewSet


class BookingSerializer(serializers.ModelSerializer):

    room_number = serializers.PrimaryKeyRelatedField(
        queryset=RoomViewSet.queryset
    )

    user = serializers.PrimaryKeyRelatedField(
        queryset=UserViewSet.queryset,
        allow_null=True,
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
