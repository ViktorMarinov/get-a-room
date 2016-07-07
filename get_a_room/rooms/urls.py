from rooms import room_views, booking_views

from django.conf.urls import url, include

from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'rooms', room_views.RoomViewSet)
router.register(r'bookings', booking_views.BookingViewSet)

urlpatterns = [
    url(
        r'^',
        include(router.urls)
    ),
]
