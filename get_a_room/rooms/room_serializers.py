from rooms.models import Room

from rest_framework import serializers


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for Room model with all fields.
    """
    class Meta:
        model = Room
        fields = ('url', 'number', 'capacity', 'is_computer_room')


class SimpleRoomSerializer(serializers.ModelSerializer):
    """
    Another serializer for Room model with fewer fields.
    """
    class Meta:
        model = Room
        fields = ('url', 'number')
