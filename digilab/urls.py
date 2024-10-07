from django.urls import path
from .views import HomeView,AboutView,PatientProfileView, PatientRegisterView, LabPersonnelRegisterView, DoctorRegisterView
from .views import PatientListView, LabPersonnelListView, DoctorListView, TestAvailableListView, TestResultListView,LabPersonnelProfileListView, UpdateTestListView, OngoingTestListView, CompletedTestListView,PaymentRequestListView, BroadcastedRequestListView,MedicalHistoryListView, PaymentView,RequestNewTestView
from django.contrib.auth import views as auth_views
from .views import RegisterView, ContactView 
from .views import DashboardView,LoginView


urlpatterns = [ 
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('', HomeView.as_view(), name='digilab/home'),  
    path('about/', AboutView.as_view(), name='digilab/about'),
    path('register/', RegisterView.as_view(), name='digilab/register'), 
    path('contact/', ContactView.as_view(), name='digilab/contact'),
    path('patients/', PatientListView.as_view(), name='digilab/patient'),
    path('lab-personnel/', LabPersonnelListView.as_view(), name='digilab/labpersonnel'),
    path('doctors/', DoctorListView.as_view(), name='digilab/doctor'),
    path('tests/', TestAvailableListView.as_view(), name='digilab/testavailable'),
    path('test-results/', TestResultListView.as_view(), name='digilab/testresult'),  
    path('lab-personnel/profile', LabPersonnelProfileListView.as_view(), name='digilab/lab-personnel/profile'),
    path('lab-personnel/update_test', UpdateTestListView.as_view(), name='digilab/lab-personnel/update_test'),
    path('lab-personnel/ongoing_tests', OngoingTestListView.as_view(), name='digilab/lab-personnel/ongoing_tests'),
    path('lab-personnel/completed_tests', CompletedTestListView.as_view(), name='digilab/lab-personnel/completed_tests'),
    path('lab-personnel/request_payment/', PaymentRequestListView.as_view(), name='digilab/lab-personnel/request_payment'),
    path('lab-personnel/broadcasted_requests/', BroadcastedRequestListView.as_view(), name='digilab/lab-personnel/broadcasted_requests'),
    path('patients/test_available/', TestAvailableListView.as_view(), name='digilab/patient/test_available'),
    path('patients/test_results/', TestResultListView.as_view(), name='digilab/patient/test_results'),
    path('patients/request_new_test', RequestNewTestView.as_view(), name='digilab/patient/request_new_test'),
    path('patients/medical_history/', MedicalHistoryListView.as_view(), name='digilab/patient/medical_history'),
    path('patients/payment/', PaymentView.as_view(), name='digilab/patient/payment'),
    path('patients/profile/', PatientProfileView.as_view(), name='digilab/patient/profile'),
    
    path('Register/patient/', PatientRegisterView.as_view(), name='digilab/registration/patient_register'),
    path('Register/lab-personnel/', LabPersonnelRegisterView.as_view(), name='digilab/registration/lab-personnel_register'),
    path('Register/doctor/', DoctorRegisterView.as_view(), name='digilab/registration/doctor_register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),



  

]

