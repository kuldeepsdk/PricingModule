from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from API import utils
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin', views.Admin, name='admin'),
    path('driver', views.Driver, name='driver'),
    path('user/<path:travelid>', views.User, name='user'),
]