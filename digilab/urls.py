from django.urls import path
from .views import HomeView,AboutView
from .views import PatientListView, LabPersonnelListView, DoctorListView, TestAvailableListView, TestResultListView

urlpatterns = [ 
    path('', HomeView.as_view(), name='digilab/home'),  
    path('about/', AboutView.as_view(), name='digilab/about'),
    path('patients/', PatientListView.as_view(), name='digilab/patient'),
    path('lab-personnel/', LabPersonnelListView.as_view(), name='digilab/labpersonnel'),
    path('doctors/', DoctorListView.as_view(), name='digilab/doctor'),
    path('tests/', TestAvailableListView.as_view(), name='digilab/testavailable'),
    path('test-results/', TestResultListView.as_view(), name='digilab/testresult'),  
]
