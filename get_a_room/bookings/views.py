from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from bookings.models import Booking
from bookings.serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed.
    """
    queryset = Booking.objects.all().order_by('start_date')
    serializer_class = BookingSerializer

    """
    Endpoint for creating bookings.
    """
    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('bookings.add_booking'):
            body = {"details": "No permission to create bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)
        request.data['user'] = user.id
        return super(BookingViewSet, self).create(request, *args, **kwargs)

    """
    Endpoint for updating bookings.
    """
    def update(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('bookings.change_booking'):
            body = {"details": "No permission to update bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        if instance.user_id != user.id:
            body = {"details": "No permission to update this booking"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        return super(BookingViewSet, self).update(request, *args, **kwargs)

    """
    Endpoint for deleting bookings.
    """
    def destroy(self, request, *args, **kwargs):
        user = request.user
        if not user.has_perm('bookings.delete_booking'):
            body = {"details": "No permission to delete bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)
        instance = self.get_object()

        if instance.user_id != user.id:
            body = {"details": "No permission to delete this booking"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        return super(BookingViewSet, self).update(request, *args, **kwargs)
