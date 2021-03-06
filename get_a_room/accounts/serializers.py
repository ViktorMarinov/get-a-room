from django.contrib.auth.models import Group
from accounts.models import User
from rest_framework import serializers


class SimpleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'role')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)
