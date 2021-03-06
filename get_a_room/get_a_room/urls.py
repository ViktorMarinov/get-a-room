from django.conf.urls import url, include
from django.contrib import admin


urlpatterns = [
    url(
        r'^admin/',
        admin.site.urls
    ),
    url(
        r'^accounts/',
        include('accounts.urls')
    ),
    url(
        r'^rooms/',
        include('rooms.urls')
    ),
    url(
        r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')
    )
]
