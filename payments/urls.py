from django.urls import path
from . import views

urlpatterns = [
    path('do_get/', views.do_get, name='do_get'),
]
