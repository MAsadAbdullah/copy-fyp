from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
import time
from django.utils import timezone
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    license_no = models.CharField(max_length=50)
    specialty = models.CharField(max_length=100)
    start_year = models.PositiveIntegerField()
    clinic_address = models.TextField()
    country = models.CharField(max_length=50)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'license_no', 'specialty', 'start_year', 'clinic_address', 'country']

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='customuser_groups_set'  # Use a unique related_name
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_permissions_set'  # Use a unique related_name
    )

    def __str__(self):
        return self.email



class Patient(models.Model):
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    cnic = models.CharField(max_length=15)
    is_minor = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    previous_medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    family_medical_history = models.TextField(blank=True)
    image_metadata = models.TextField(blank=True)
    doctor_remarks = models.TextField(blank=True)
    privacy_policy_agreement = models.BooleanField()
    left_eye_fundus_image = models.ImageField(upload_to='fundus_images/', max_length=250, null=True, default=None)
    right_eye_fundus_image = models.ImageField(upload_to='fundus_images/', max_length=250, null=True, default=None)
    added_by_id = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    arival_date_time = models.DateTimeField(auto_now_add=True)
    left_eye_result = models.CharField(max_length=100, blank=True, default='')
    right_eye_result = models.CharField(max_length=100, blank=True, default='')
    

    def save(self, *args, **kwargs):
        # if not self.pk:
            
            # print("I am here at post 1")
            # if hasattr(self, 'request'):
            #     print("I am here at post 2")
            #     if hasattr(self.request, 'added_by_id'):
            #         self.added_by_id = self.request.user  # Assign added_by_id here
            #         print("I am here at post 3")
            # else:
            #     self.added_by_id = None  # Handle cases where request.user is not available
            #     print("I am here at post 4")
        super(Patient, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    
