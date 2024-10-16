from django.urls import path
from . import views

urlpatterns = [
    path('online/lipa/', views.lipa_na_mpesa_online, name='lipa_na_mpesa')
]