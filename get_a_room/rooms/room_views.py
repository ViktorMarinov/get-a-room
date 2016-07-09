import datetime

from rooms.models import Room, Booking
from rooms.room_serializers import RoomSerializer
from rooms.my_fields import DAYS_OF_THE_WEEK

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response


class RoomViewSet(viewsets.ModelViewSet):
    """
    API view set for Room model. Contains multiple views.
    Can list all room or room details
    """
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer

    @list_route(methods=['get'])
    def filter(self, request):
        """
        Endpoint for filtering rooms by given query params
        """

        ALLOWED_PARAMS = ['is_computer_room', 'capacity', 'min_capacity']
        params = request.query_params.dict()
        filter_params = {}
        for key in params:
            if key in ALLOWED_PARAMS:
                if key == 'is_computer_room':
                    filter_params[key] = params[key] == 'true'
                elif key == 'min_capacity':
                    filter_params['capacity__gte'] = int(params[key])
                else:
                    filter_params[key] = params[key]

        try:
            filtered_set = Room.objects.filter(**filter_params)
        except:
            return Response(
                {'details': 'Invalid query params'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer = RoomSerializer(
            filtered_set, context={'request': request}, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def find(self, request):
        """
        Endpoint for finding free rooms for given dates and times.
        If no end_date is given, the search is made for the start date only
        Additional parameters:
            * is_computer_room : filter results by is_computer_room property
            * min_capacity : minimum capacity for the room
        """

        params = request.query_params.dict()
        start_date = datetime.datetime.strptime(
            params['start_date'], "%Y-%m-%d").date()
        try:
            end_date = datetime.datetime.strptime(
                params['end_date'], "%Y-%m-%d").date()
        except KeyError:
            end_date = start_date
        start_time = datetime.datetime.strptime(
            params['start'], "%H:%M").time()
        end_time = datetime.datetime.strptime(params['end'], "%H:%M").time()
        filter_params = {}
        try:
            filter_params['is_computer_room'] = (
                params['is_computer_room'] == 'true')
        except KeyError:
            pass
        try:
            filter_params['capacity__gte'] = int(params['min_capacity'])
        except (KeyError, ValueError):
            pass
        rooms = Room.objects.filter(**filter_params)
        result = []
        for room in rooms:
            bookings = Booking.objects.filter(room_number=room.number)
            is_free = True
            for booking in bookings:
                if (booking.start_date <= end_date and
                   booking.end_date >= start_date and
                   booking.day_of_week == DAYS_OF_THE_WEEK[
                        start_date.weekday()][0]):
                    if (booking.end_time > start_time and
                       booking.start_time < end_time):
                        is_free = False
                        break
            if is_free:
                result.append(room.number)

        result_queryset = Room.objects.filter(number__in=result)
        serializer = RoomSerializer(
            result_queryset, context={'request': request}, many=True)
        return Response(serializer.data)
