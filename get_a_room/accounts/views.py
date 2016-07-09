from django.contrib.auth.models import Group

from accounts.models import User
from accounts.serializers import UserSerializer, GroupSerializer
from accounts.serializers import SimpleUserSerializer

from rest_framework import filters
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import detail_route, list_route
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed as list or by id.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    http_method_names = ['get', 'head', 'options']

    @list_route()
    def filter(self, request):
        """
        Filter users by the given query params.
        """
        ALLOWED_PARAMS = {'username', 'role'}
        params = request.query_params.dict()
        params = {
            key: params[key] for key in params if key in ALLOWED_PARAMS
        }
        try:
            filtered_set = User.objects.filter(**params)
        except:
            return Response(
                {'details': 'Invalid query params'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(
            filtered_set, context={'request': request}, many=True)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed as list or by id.
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
@permission_classes((AllowAny,))
def register(request):
    """
    Endpoint for registration.
    Does not require any permissions, so that anyone can access it.
    """
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
