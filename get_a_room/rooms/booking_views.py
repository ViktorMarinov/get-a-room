import datetime
from rooms.my_fields import DAYS_OF_THE_WEEK

from rooms.models import Booking
from rooms.booking_serializers import BookingSerializer

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookings to be viewed.
    """
    queryset = Booking.objects.all().order_by('start_date')
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        """
        Endpoint for creating bookings.
        """
        user = request.user
        if not user.has_perm('bookings.add_booking'):
            body = {"details": "No permission to create bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = user.username
        return super(BookingViewSet, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Endpoint for updating bookings.
        """
        user = request.user
        if not user.has_perm('bookings.change_booking'):
            body = {"details": "No permission to update bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        print(request.data)
        instance = self.get_object()
        if instance.user_id != user.id:
            body = {"details": "No permission to update this booking"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)
        request.data['room_number'] = instance.room_number.number
        return super(BookingViewSet, self).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Endpoint for deleting bookings.
        """
        user = request.user
        if not user.has_perm('bookings.delete_booking'):
            body = {"details": "No permission to delete bookings"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        instance = self.get_object()
        if instance.user_id != user.id:
            body = {"details": "No permission to delete this booking"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        return super(BookingViewSet, self).destroy(request, *args, **kwargs)

    @list_route(methods=['get'])
    def filter(self, request):
        """
        Endpoint for filtering bookings by given query parameters
        """
        ALLOWED_PARAMS = {'room_number', 'user', 'start_date',
                          'end_date', 'day_of_week', 'start_time', 'end_time'}
        params = request.query_params.dict()
        params = {
            key: params[key] for key in params if key in ALLOWED_PARAMS
        }
        try:
            filtered_set = Booking.objects.filter(**params)
        except:
            return Response(
                {'details': 'Invalid query params'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = BookingSerializer(
            filtered_set, context={'request': request}, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def ondate(self, request):
        """
        Endpoint for filtering booking for given date
        """
        params = request.query_params.dict()
        try:
            date = datetime.datetime.strptime(
                params['date'], "%Y-%m-%d").date()
            day_of_week = DAYS_OF_THE_WEEK[date.weekday()][0]
            bookings = Booking.objects.filter(
                start_date__lte=date,
                end_date__gte=date,
                day_of_week=day_of_week
            )
        except:
            return Response(
                {'details': 'Invalid query params'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = BookingSerializer(
            bookings, context={'request': request}, many=True)
        return Response(serializer.data)
