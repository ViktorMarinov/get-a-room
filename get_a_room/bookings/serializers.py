from rest_framework import serializers

from bookings.models import Booking

from accounts.views import UserViewSet

from rooms.views import RoomViewSet


class BookingSerializer(serializers.ModelSerializer):

    room_number = serializers.PrimaryKeyRelatedField(
        queryset=RoomViewSet.queryset
    )

    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        print("Entered serializer validata!")
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
