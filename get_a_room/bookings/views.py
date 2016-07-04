from rest_framework import viewsets
from rest_framework.views import APIView

from bookings.models import Booking
from bookings.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed or edited.
    """
    queryset = Booking.objects.all().order_by('start_date')
    serializer_class = BookingSerializer
