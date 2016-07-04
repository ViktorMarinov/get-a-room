from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from accounts.models import User
from accounts.serializers import UserSerializer, GroupSerializer
from accounts.serializers import SimpleUserSerializer

from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'options']

    @list_route()
    def getuser(self, request):
        username = request.query_params.get('username', None)
        if username is not None:
            user = get_object_or_404(User, username=username)
            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAdminUser,)
    http_method_names = ['get', 'head', 'options']

    @detail_route(methods=['get'])
    def members(self, request, pk=None):
        """
        Returns a list of the members of the group
        """
        group = self.get_object()
        members = group.user_set.all()
        serializer = SimpleUserSerializer(
            members,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)


@api_view(['POST', 'GET'])
def register(request):
    USER_FIELDS = ['username', 'password', 'email', 'role']
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid(raise_exception=True):
        user_data = {
            field: data
            for (field, data) in request.data.items()
            if field in USER_FIELDS
        }
        user = User.objects.create_user(
            **user_data
        )

        return Response(
            UserSerializer(instance=user, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )
