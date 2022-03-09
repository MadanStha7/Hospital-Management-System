from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.contrib.auth.models import Group


class User(AbstractUser):
    """
    Model to store the django built in User model
    """

    email = models.EmailField(("Email"), max_length=254, unique=True)
    username = models.CharField(
        ("Username"), max_length=50, unique=True, null=True, blank=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.id}--{self.email}"


class Patient(models.Model):
    """
    Model to store the patients details
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    full_name = models.CharField(("Full Name"), max_length=50)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(("Date of birth"), null=True)
    image = models.ImageField(upload_to="patient")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Patient")
        print("GROUP", group)
        print("user", self.user)
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        ordering = ["-id"]


class Doctor(models.Model):
    """
    Model to store the Doctor details
    """

    SHIFT = (
        ("M", "Morning"),
        ("E", "Evening"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    full_name = models.CharField(("Full Name"), max_length=50)
    hospital_name = models.CharField(("Hospital Name"), max_length=80)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=15, blank=True, null=True)
    shift = models.CharField(choices=SHIFT, max_length=2, null=True, blank=True)
    location = models.CharField(max_length=100)
    dob = models.DateField(("Date of birth"), null=True)
    image = models.ImageField(upload_to="patient")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Doctor")
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}"

    class Meta:
        ordering = ["-id"]
