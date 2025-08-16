from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime

# Create your models here.
STATUS_CHOICES = [
    ('PENDING',   'Pending'),
    ('CONFIRMED', 'Confirmed'),
    ('CANCELLED', 'Cancelled'),
]

WEEKDAY_CHOICES = [
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    ]

class Availability(models.Model):
    """
    Represents a single time slot on a calendar date, tracking whether it
    can be booked, is already booked, or has been marked unavailable.

    Fields:
        date (date):
            The calendar date for this slot. Defaults to today.
        start_time (time):
            The start time of the slot.
        end_time (time):
            The end time of the slot.
        unavailable (bool):
            If True, this slot cannot be booked (e.g. a blackout period).
        is_booked (bool):
            If True, this slot has already been booked by a user.
    """
    date = models.DateField(default=datetime.date.today)

    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")

    unavailable = models.BooleanField(
        default=False, help_text="Mark this slot as unavailable for booking.")
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        status = "Unavailable" if self.unavailable else (
            "Booked" if self.is_booked else "Available")
        return f"{self.date} {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')} ({status})"

class Weekday(models.Model):
    """
    Represents a day of the week by its numeric code and name.

    Fields:
        number (int):
            The numeric identifier for the weekday (e.g., 0=Monday, 6=Sunday),
            constrained by WEEKDAY_CHOICES and unique across entries.
        name (str):
            The human-readable name of the weekday (e.g., "Monday"), up to 9 characters.
    """
    number = models.IntegerField(choices=WEEKDAY_CHOICES, unique=True)
    name   = models.CharField(max_length=9)

    def __str__(self):
        return self.name

class AvailabilityBlock(models.Model):
    """
    Defines a recurring time block over a date range and specific weekdays.

    Fields:
        start_date (date):
            The first calendar date on which this block becomes active.
            Defaults to today's date.
        end_date (date):
            The last calendar date on which this block remains active.
            Defaults to today's date.
        start_time (time):
            The daily starting time of the block.
        end_time (time):
            The daily ending time of the block.
        days_of_week (ManyToMany[Weekday]):
            The set of weekdays on which this block applies. If empty,
            the block is considered for all days in the date range.

    __str__:
        Returns a human-readable description including date range,
        time interval, and the names of the applicable weekdays.
    """
    start_date   = models.DateField(default=datetime.date.today)
    end_date     = models.DateField(default=datetime.date.today)
    start_time = models.TimeField()
    end_time = models.TimeField()

    days_of_week = models.ManyToManyField(
        Weekday,
        blank=True,
        help_text="Which days of the week this block applies to",
    )

    def __str__(self):
        days = ", ".join(d.name for d in self.days_of_week.all())
        return (f"{self.start_date} → {self.end_date} "
                f"@ {self.start_time.strftime('%H:%M')}–{self.end_time.strftime('%H:%M')} "
                f"on {days}")


class Booking(models.Model):
    """
    Represents a user’s appointment booking for a specific availability slot.

    Fields:
        user (ForeignKey to AUTH_USER_MODEL):
            The user who made the booking. Deleting the user cascades to their bookings.
        availability (OneToOneField to Availability):
            The pre-generated time slot occupied by this booking. Protected from deletion.
        treatment (ForeignKey to services.Treatment):
            The selected treatment for this booking. Protected from deletion.
        notes (TextField):
            Optional free-form notes provided by the user.
        created_at (DateTimeField):
            Timestamp when this booking was first created.
        updated_at (DateTimeField):
            Timestamp when this booking was last modified.
        status (CharField):
            Current status of the booking; one of STATUS_CHOICES, defaults to 'PENDING'.

    Meta:
        ordering:  Newest bookings first (descending created_at).
        verbose_name: 'Booking'
        verbose_name_plural: 'Bookings'

    __str__:
        Returns a concise description including user, treatment, date, and start time.

    Methods:
        has_conflict(cls, date, start_time, end_time, exclude_booking_id=None):
            Class method to detect overlap between a proposed time range and existing bookings
            on the same date, optionally excluding one booking (e.g. when editing).

        clean(self):
            Model validation hook that raises a ValidationError if the chosen slot
            is already marked as booked.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    # each slot can only be booked once
    availability = models.OneToOneField(
        Availability,
        on_delete=models.PROTECT,
        related_name="booking",
        null=True, blank=True,
        help_text="Which pre‐generated slot this booking occupies."
    )
    treatment = models.ForeignKey(
        'services.Treatment', on_delete=models.PROTECT, null=True,
    blank=True, related_name='bookings')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'


    def __str__(self):
        slot = self.availability
        return (f"Booking for {self.user} - {self.treatment} on "
                f"{slot.date} from {slot.start_time.strftime('%H:%M')}")

    @classmethod
    # checking all bookings so cls is used instead of self.
    def has_conflict(cls, date, start_time, end_time, exclude_booking_id=None):
        # check to see if a new booking would conflict with existing bookings
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
        if self.availability and self.availability.is_booked:
            raise ValidationError("This time slot conflicts with an existing booking.")
