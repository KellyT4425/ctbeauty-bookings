from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Availability(models.Model):
    date = models.DateField(default=datetime.date.today)

    start_time = models.TimeField()
    end_time = models.TimeField()

    unavailable = models.BooleanField(
        default=False, help_text="Mark this slot as unavailable for booking.")
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        status = "Booked" if self.is_booked else "Available"
        return f"{self.date} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')} ({status})"


class AvailabilityBlock(models.Model):
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} from {self.start_time} to {self.end_time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # each slot can only be booked once
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE)
    # treatment = models.ForeignKey(
    # 'Treatment', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.user} on {self.availability.date} at {self.availability.start_time}"
