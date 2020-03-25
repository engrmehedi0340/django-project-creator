from django.urls import path
from . import views

urlpatterns = [
 path('', views.home, name='home'),
 path('home', views.home, name='home'),
 path('action', views.action, name='action'),
 path('run_server', views.run_server, name='run_server'),
]

