from rest_framework import serializers
from rooms.models import Room


class RoomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'number', 'capacity', 'is_computer_room')


class SimpleRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('url', 'number')
