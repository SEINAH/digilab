"""
URL configuration for digital_lab project.

"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('digilab.urls')),
<<<<<<< HEAD
    path('mpesa/', include('mpesa_api.urls')),  # include the mpesa app's URL patterns

=======
    path('/mpesa', include('mpesa_api.urls')),
>>>>>>> 1365f20a6aa31d11912fb28eba2eb8b7ffec67a2

]
