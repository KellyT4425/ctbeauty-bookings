from django.db import models
from django.contrib.auth.models import User

# Create your models here.

STATUS = [('confirmed', 'Confirmed'),
          ('cancelled', 'Cancelled'),
          ('completed', 'Completed'),]


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointment_booker")
    treatment = models.ForeignKey(
        Treatment, on_delete=models.CASCADE, related_name="treatment_option")
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('date', 'time')


class Availability(models.Model):
    day_of_week = models.CharField(max_length=9, choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wedenday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ])

    start_time = models.TimeField()
    end_time = models.TimeField()

    unavilable = models.BooleanField(
        default=False, help_text="Mark this slot as unavailable for booking.")
    is_active = models.BooleanField(
        default=True, help_text="Set to False to temporarily disable this availability.")

    def __str__(self):
        return f"{self.day_of_week}: {self.start_time} - {self.end_time}"
