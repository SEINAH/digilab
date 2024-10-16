"""
URL configuration for digital_lab project.

"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('digilab.urls')),
    path('/mpesa', include('mpesa_api.urls')),

]
