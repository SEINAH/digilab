from django.contrib import admin
from .models import Patient, LabPersonnel, Doctor, TestAvailable, TestResult

# Register each model with the admin site
admin.site.register(Patient)
admin.site.register(LabPersonnel)
admin.site.register(Doctor)
admin.site.register(TestAvailable)
admin.site.register(TestResult)


