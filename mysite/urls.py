from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from mysite.core import views as core_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mysite.core.urls')),
]
