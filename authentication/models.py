from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model inheriting from AbstractUser
class CustomUser(AbstractUser):
    # Add related_name attributes to avoid conflicts
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Changed related name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',  # Changed related name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

# UserProfile model to store additional user information
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # Link to CustomUser
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=255, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(blank=True)  # Optional bio

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "User Profiles"
