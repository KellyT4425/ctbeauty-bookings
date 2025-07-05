from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
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

class Weekday(models.Model):
    number = models.IntegerField(choices=WEEKDAY_CHOICES, unique=True)
    name   = models.CharField(max_length=9)

    def __str__(self):
        return self.name

class AvailabilityBlock(models.Model):
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
        """Django calls this to validate the model before saving"""
        from django.core.exceptions import ValidationError

        if self.availability.is_booked:
            raise ValidationError(
                "This time slot conflicts with an existing booking.")
