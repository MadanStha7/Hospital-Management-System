from django.db import models
from django.contrib.auth.models import User

USER_TYPE = (
    ("Patient", "Patient"),
    ("Hospital", "Hospital"),
    ("Doctor", "Doctor"),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE, default="Patient")
    phone_number = models.CharField(max_length=10, blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
