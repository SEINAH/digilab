from django.views.generic import ListView,TemplateView
from django.utils import timezone
from .models import Patient, LabPersonnel, Doctor, TestAvailable, TestResult,LabPersonnelProfile,Test, OngoingTest, CompletedTest, PaymentRequest, BroadcastedRequest,MedicalHistory,PatientProfile
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PatientRegistrationForm, LabPersonnelRegistrationForm, DoctorRegistrationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = 'digilab/home.html'

class AboutView(TemplateView):
    template_name = 'digilab/about.html'  

class RegisterView(TemplateView):
    template_name = 'digilab/register.html'  

class ContactView(TemplateView):
    template_name = 'digilab/contact.html'       

class PatientListView(ListView):
    model = Patient
    template_name = 'digilab/patient.html'
    context_object_name = 'patients'

class LabPersonnelListView(ListView):
    model = LabPersonnel 
    template_name = 'digilab/labpersonnel.html'
    context_object_name = 'labpersonnels'

class DoctorListView(ListView):
    model = Doctor
    template_name = 'digilab/doctor.html'
    context_object_name = 'doctors'

class LabPersonnelProfileListView(ListView):
    model = LabPersonnelProfile
    template_name = 'digilab/lab-personnel/profile.html'
    context_object_name = 'lab-personnel/profile'

    def get_object(self):
        return LabPersonnelProfile.objects.get(user=self.request.user)
    
# List view for updating tests (you can display all tests or filter those eligible for updating)
class UpdateTestListView(ListView):
    model = Test
    template_name = 'digilab/lab-personnel/update_test.html'  
    context_object_name = 'lab-personnel/update_test'

    def get_queryset(self):
        # You can filter tests by status (e.g., 'pending') if only those need to be updated
        return Test.objects.filter(status='pending')

# List view for ongoing tests
class OngoingTestListView(ListView):
    model = OngoingTest
    template_name = 'digilab/lab-personnel/ongoing_tests.html'  # path to your template
    context_object_name = 'lab-personnel/ongoing_tests'

    def get_queryset(self):
        # Only fetch tests that are ongoing
        return OngoingTest.objects.filter(test__status='ongoing')

# List view for completed tests
class CompletedTestListView(ListView):
    model = CompletedTest
    template_name = 'digilab/lab-personnel/completed_tests.html'  # path to your template
    context_object_name = 'lab-personnel/completed_tests'

    def get_queryset(self):
        # Only fetch tests that are completed
        return CompletedTest.objects.filter(test__status='completed')
    
class PaymentRequestListView(ListView):
    model = PaymentRequest
    template_name = 'digilab/lab-personnel/request_payment.html'
    context_object_name = 'lab-personnel/payment_requests'

    def get_queryset(self):
        # Customize query if needed
        return PaymentRequest.objects.filter(is_paid=False)

class BroadcastedRequestListView(ListView):
    model = BroadcastedRequest
    template_name = 'digilab/lab-personnel/broadcasted_requests.html'
    context_object_name = 'lab-personnel/broadcasted_requests'

    def get_queryset(self):
        # Customize query if needed, example filtering by date
        return BroadcastedRequest.objects.all().order_by('-broadcasted_at')

class TestAvailableListView(ListView):
    model = TestAvailable
    template_name = 'digilab/patient/test_available.html'
    context_object_name = 'patient/tests'

class TestResultListView(ListView):
    model = TestResult
    template_name = 'digilab/patient/test_results.html'
    context_object_name = 'patient/test_results'

    #def get_queryset(self):
        #return TestResult.objects.filter(patient__user=self.request.user)

class RequestNewTestView(TemplateView):
    template_name = 'digilab/patient/request_new_test.html'

    # Add form processing logic if needed, e.g., POST request handling

class MedicalHistoryListView(ListView):
    model = MedicalHistory
    template_name = 'digilab/patient/medical_history.html'
    context_object_name = 'patient/medical_history'

    #def get_queryset(self):
        # Get the patient instance associated with the logged-in user
       # patient = self.request.user.patient  # Assuming a OneToOneField relationship with User
        # Filter medical history for that patient
        #return MedicalHistory.objects.filter(patient=patient)

class PaymentView(ListView):
    model = PaymentRequest
    template_name = 'digilab/patient/payment.html'
    context_object_name = 'patient/payment'

   # def get_queryset(self):
        #return PaymentRequest.objects.filter(patient__user=self.request.user)
    
class PatientProfileView(TemplateView):
    model = PatientProfile
    template_name = 'digilab/patient/profile.html'
    context_object_name = 'profile'

    #def get_context_data(self, **kwargs):
        #context = super().get_context_data(**kwargs)
        # Get the patient profile for the logged-in user
       # context['profile'] = PatientProfile.objects.get(patient=self.request.user.patient)
        #return context
# digilab/views.py

from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import login
from .models import Patient, LabPersonnel, Doctor, User
from .forms import PatientRegistrationForm, LabPersonnelRegistrationForm, DoctorRegistrationForm

class PatientRegisterView(CreateView):
    model = User
    form_class = PatientRegistrationForm
    template_name = 'digilab/registration/patient_register.html'
    success_url = reverse_lazy('patient_dashboard')

    def form_valid(self, form):
        # Save the form but don't commit the user to the database yet
        user = form.save(commit=False)
        user.user_type = 'patient'
        user.save()  # Save the user now
        # Create the associated Patient profile
        Patient.objects.create(user=user)
        # Log the user in
        login(self.request, user)
        return redirect(self.success_url)
    
class LabPersonnelRegisterView(CreateView):
    model = User
    form_class = LabPersonnelRegistrationForm
    template_name = 'digilab/registration/labpersonnel_register.html'
    success_url = reverse_lazy('labpersonnel_dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'labpersonnel'
        user.save()
        LabPersonnel.objects.create(user=user)
        login(self.request, user)
        return redirect(self.success_url)


class DoctorRegisterView(CreateView):
    model = User
    form_class = DoctorRegistrationForm
    template_name = 'digilab/registration/doctor_register.html'
    success_url = reverse_lazy('doctor_dashboard')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.user_type = 'doctor'
        user.save()
        Doctor.objects.create(user=user)
        login(self.request, user)
        return redirect(self.success_url)


    
class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if request.user.user_type == 'patient':
            return redirect('digilab/patient.html')
        elif request.user.user_type == 'labpersonnel':
            return redirect('labpersonnel_dashboard')
        elif request.user.user_type == 'doctor':
            return redirect('doctor_dashboard')