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

    BLOOD_GROUP = [
        ("-A", "-A"),
        ("+A", "+A"),
        ("-B", "-B"),
        ("+B", "+B"),
        ("-AB", "-AB"),
        ("+AB", "+AB"),
        ("-O", "-O"),
        ("+O", "+O"),
    ]

    GENDER = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient")
    full_name = models.CharField(("Full Name"), max_length=50)
    health_uid = models.CharField(max_length=16, null=True, blank=True)
    phone = models.CharField(max_length=15)
    dob = models.DateField(("Date of birth"), null=True)
    blood_group = models.CharField(choices=BLOOD_GROUP, max_length=5, null=True)
    gender = models.CharField(max_length=100, choices=GENDER, null=True)
    image = models.ImageField(upload_to="patient", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Patient")
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
    status = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(("Full Name"), max_length=50)
    hospital_name = models.CharField(("Hospital Name"), max_length=80)
    phone = models.CharField(max_length=15)
    shift = models.CharField(choices=SHIFT, max_length=2, null=True, blank=True)
    location = models.CharField(max_length=100)
    dob = models.DateField(("Date of birth"), null=True)
    image = models.ImageField(upload_to="doctor",null=True,blank=True)
    experience = models.CharField(max_length=100, null=True)
    specialist = models.CharField(max_length=100, null=True)
    clinic = models.CharField(max_length=100, null=True, blank=True)
    timing = models.CharField(max_length=100, null=True)
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



class Appointment(models.Model):
    """
    Model to store the appointment records between doctors and patient
    """
    STATUS = (
        ("P", "Pending"),
        ("A", "Approve"),
    )

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="appointment")
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE,related_name="appointment")
    app_date = models.DateTimeField()
    status = models.CharField(choices=STATUS, max_length=2, null=True, blank=True)
    

    def __str__(self):
        return f"{self.doctor.full_name}--{self.patient.full_name}"

    class Meta:
        ordering = ["-id"]


