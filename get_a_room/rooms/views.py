from rooms.models import Room
from rest_framework import viewsets
from rooms.serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer
