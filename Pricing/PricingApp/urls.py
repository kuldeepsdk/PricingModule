from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from API import utils
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin', views.Admin, name='Admin'),
    path('Driver', views.Driver, name='Driver'),
    path('User', views.User, name='User'),
]