from django.conf.urls import url, include
from rest_framework import routers
from rooms import views


router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet)

urlpatterns = [
    url(
        r'^',
        include(router.urls)
    ),
]
