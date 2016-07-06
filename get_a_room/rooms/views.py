from rooms.models import Room
from rooms.serializers import RoomSerializer

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response


class RoomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rooms to be viewed or edited.
    """
    queryset = Room.objects.all().order_by('number')
    serializer_class = RoomSerializer

    @list_route()
    def filter(self, request):
        params = request.query_params.dict()
        print(params)
        filtered_set = Room.objects.filter(**params)
        print(filtered_set)
        serializer = RoomSerializer(
            filtered_set, context={'request': request}, many=True)
        return Response(serializer.data)
