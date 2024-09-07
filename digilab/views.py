from django.views.generic import ListView,TemplateView
from .models import Patient, LabPersonnel, Doctor, TestAvailable, TestResult

class HomeView(TemplateView):
    template_name = 'digilab/home.html'

class AboutView(TemplateView):
    template_name = 'digilab/about.html'    

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

class TestAvailableListView(ListView):
    model = TestAvailable
    template_name = 'digilab/testavailable.html'
    context_object_name = 'tests'

class TestResultListView(ListView):
    model = TestResult
    template_name = 'digilab/testresult.html'
    context_object_name = 'test_results'
