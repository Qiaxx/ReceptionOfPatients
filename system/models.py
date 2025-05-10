from django.db import models
from django.conf import settings

class Region(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"
