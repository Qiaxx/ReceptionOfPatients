from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


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

class Doctor(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    middle_name = models.CharField("Отчество", max_length=50, blank=True)
    specialization = models.CharField("Специальность", max_length=100)
    experience_years = models.PositiveIntegerField("Стаж (в годах)")
    photo = models.ImageField(upload_to='doctors/photos/', null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.specialization})"


class AppointmentSlot(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='slots')
    date = models.DateField("Дата приема", blank=True, null=True)
    time = models.TimeField("Время приема", blank=True, null=True)
    duration_minutes = models.PositiveIntegerField("Длительность приема (мин)", default=30)
    is_booked = models.BooleanField("Занято", default=False)

    class Meta:
        ordering = ['date', 'time']
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.doctor} — {self.date} в {self.time.strftime('%H:%M')}"

    def start_datetime(self):
        return timezone.make_aware(datetime.combine(self.date, self.time))

    def end_datetime(self):
        return self.start_datetime() + timedelta(minutes=self.duration_minutes)

    def is_past(self):
        return self.start_datetime() < timezone.now()

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    slot = models.OneToOneField(AppointmentSlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
