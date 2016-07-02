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

    groups = SimpleGroupSerializer(
        many=True,
        read_only=True
    )

    def create(self, validated_data):
        user = User.objects.create(
            validated_data
        )
        user.set_password(validated_data['password'])
        user.save()

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name',)
