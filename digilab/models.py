from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class LabPersonnel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    position = models.CharField(max_length=100)
    license_upload = models.FileField(upload_to='licenses/')
    certificate_upload = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Doctor(models.Model):
   
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialty}"

class TestAvailable(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.name

class TestResult(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test = models.ForeignKey(TestAvailable, on_delete=models.CASCADE)
    result = models.TextField()
    date_performed = models.DateTimeField(auto_now_add=True)
    performed_by = models.ForeignKey(LabPersonnel, on_delete=models.CASCADE)
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.patient} - {self.test}"
    
class LabPersonnelProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    license_upload = models.FileField(upload_to='licenses/', null=True, blank=True)  # For uploading license documents
    certificate_upload = models.FileField(upload_to='certificates/', null=True, blank=True)  # For uploading certificates
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)  # Short bio for the lab personnel

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Lab Personnel"    

# Test Model
class Test(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='tests')
    test_name = models.CharField(max_length=100)
    test_description = models.TextField()
    test_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    assigned_lab_personnel = models.ForeignKey(LabPersonnel, on_delete=models.SET_NULL, null=True, related_name='assigned_tests')
    result = models.TextField(blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    def update_status(self, status):
        """Update the status of the test and completion date if completed."""
        self.status = status
        if status == 'completed':
            self.completion_date = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.test_name} for {self.patient.name}"

# OngoingTest Model
class OngoingTest(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='ongoing_test')
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ongoing test: {self.test.test_name} for {self.test.patient.name}"

# CompletedTest Model
class CompletedTest(models.Model):
    test = models.OneToOneField(Test, on_delete=models.CASCADE, related_name='completed_test')
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Completed test: {self.test.test_name} for {self.test.patient.name}"        

class PaymentRequest(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    amount_requested = models.DecimalField(max_digits=10, decimal_places=2)
    requested_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment Request for {self.test.test_name} - Amount: {self.amount_requested}"

class BroadcastedRequest(models.Model):
    lab_personnel = models.ForeignKey('LabPersonnel', on_delete=models.CASCADE)
    message = models.TextField()
    broadcasted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Broadcasted Request by {self.lab_personnel.name} at {self.broadcasted_at}"

class TestRequest(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_type = models.CharField(max_length=255)
    test_details = models.TextField()
    requested_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=255)
    payment_date = models.DateTimeField(auto_now_add=True)   

class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_history')
    condition = models.CharField(max_length=255, help_text="Enter the medical condition")
    diagnosis_date = models.DateField(null=True, blank=True)
    medications = models.TextField(null=True, blank=True, help_text="List medications taken for this condition")
    allergies = models.TextField(null=True, blank=True, help_text="List any known allergies")
    treatments = models.TextField(null=True, blank=True, help_text="Describe past treatments, surgeries, or therapy")
    doctor_notes = models.TextField(null=True, blank=True, help_text="Any additional notes from the doctor")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Medical History for {self.patient.name} - Condition: {self.condition}"   

class PatientProfile(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='profile')
    address = models.CharField(max_length=255, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile for {self.patient.name}"    
    
    #forms
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .models import Test

class TestUpdateView(UpdateView):
    model = Test
    fields = ['result', 'status']  # Fields to be updated
    template_name = 'update_test.html'
    context_object_name = 'test'
    
    # Define the success URL after updating the test
    def get_success_url(self):
        return reverse_lazy('test_list')  # Adjust as per your URL names
