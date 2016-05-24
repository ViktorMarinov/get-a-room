from rest_framework import serializers

from bookings.models import Booking

from accounts.views import UserViewSet

from rooms.views import RoomViewSet


class BookingSerializer(serializers.ModelSerializer):

    room_number = serializers.PrimaryKeyRelatedField(
        queryset=RoomViewSet.queryset
    )

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=UserViewSet.queryset
    )

    start_date = serializers.DateField()
    end_date = serializers.DateField()

    class Meta:
        model = Booking
        fields = (
            'url',
            'room_number',
            'user_id',
            'start_date',
            'end_date',
            'start_time',
            'end_time',
            'day_of_week'
        )
