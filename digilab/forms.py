from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient, LabPersonnel, Doctor

# Patient Registration Form
class PatientRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female')], required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            patient = Patient.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                date_of_birth=self.cleaned_data['date_of_birth'],
                gender=self.cleaned_data['gender'],
                contact_number=self.cleaned_data['contact_number'],
                email=self.cleaned_data['email'],
                address=self.cleaned_data['address']
            )
            patient.save()
        return user

# Lab Personnel Registration Form
class LabPersonnelRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    employee_id = forms.CharField(max_length=20, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    position = forms.CharField(max_length=100, required=True)
    license_upload = forms.FileField(required=True)
    certificate_upload = forms.FileField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            lab_personnel = LabPersonnel.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                employee_id=self.cleaned_data['employee_id'],
                contact_number=self.cleaned_data['contact_number'],
                email=self.cleaned_data['email'],
                position=self.cleaned_data['position'],
                license_upload=self.cleaned_data['license_upload'],
                certificate_upload=self.cleaned_data['certificate_upload']
            )
            lab_personnel.save()
        return user

# Doctor Registration Form
class DoctorRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    specialty = forms.CharField(max_length=100, required=True)
    contact_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            doctor = Doctor.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                specialty=self.cleaned_data['specialty'],
                contact_number=self.cleaned_data['contact_number'],
                email=self.cleaned_data['email']
            )
            doctor.save()
        return user
