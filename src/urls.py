from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('checker.urls', namespace='checker')),
    url(r'^', include('users.urls', namespace='users')),
]
