from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


USER_TYPE = (
    ("P", "Patient"),
    ("D", "Doctor"),
)

SHIFT = (
    ("M", "Morning"),
    ("E", "Evening"),
)


class UserProfile(AbstractUser):
    """
    Model to store the details of user as there are three types of user(doctor,patient,admin)
    """

    email = models.EmailField(("Email"), max_length=254, unique=True)
    username = models.CharField(
        ("Username"), max_length=50, unique=True, null=True, blank=True
    )
    full_name = models.CharField(("Full Name"), max_length=50)
    phone = models.CharField(max_length=15)
    blood_group = models.CharField(
        max_length=15, blank=True, null=True
    )  # field for patient
    shift = models.CharField(
        choices=SHIFT, max_length=2, null=True, blank=True
    )  # field for doctors
    dob = models.DateField(("Date of birth"), null=True)
    user_type = models.CharField(
        choices=USER_TYPE,
        max_length=2,
    )
    image = models.ImageField(upload_to="user-profile")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    @property
    def is_patient(self):
        return self.user_type == "P"

    @property
    def is_doctor(self):
        print("user type", self.user_type)
        return self.user_type == "D"

    def __str__(self):
        return f"{self.email}--{self.get_user_type_display()}"
