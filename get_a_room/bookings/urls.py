from django.conf.urls import url, include
from rest_framework import routers
from bookings import views


router = routers.DefaultRouter()
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    url(
        r'^',
        include(router.urls)
    ),
]
