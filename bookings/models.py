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
        status = "Unavailable" if self.unavailable else (
            "Booked" if self.is_booked else "Available")
        return f"{self.date} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')} ({status})"
    # EDITIED


class AvailabilityBlock(models.Model):
    date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.date} from {self.start_time} to {self.end_time}"


class Booking(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_bookings")
    # each slot can only be booked once
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    treatment = models.ForeignKey(
        'services.Treatment', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Booking for {self.user} on {self.date} from {self.start_time} to {self.end_time}"

    @classmethod
    # checking all bookings so cls is used instead of self.
    def has_conflict(cls, date, start_time, end_time, exclude_booking_id=None):
        # check to se if a new booking would conflict with existing bookings
        existing_bookings = cls.objects.filter(date=date)

        # if we are updating an existing booking, dont check against itself.
        if exclude_booking_id:
            existing_bookings = existing_bookings.exclude(
                id=exclude_booking_id)

        # check each existing booking for overlap.
        for booking in existing_bookings:
            if (start_time < booking.end_time and end_time > booking.start_time):
                return True
            else:
                return False

    def clean(self):
        """Django calls this to validate the model before saving"""
        from django.core.exceptions import ValidationError

        if Booking.has_conflict(self.date, self.start_time, self.end_time, self.id):
            raise ValidationError(
                "This time slot conflicts with an existing booking.")
