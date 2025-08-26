from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import datetime

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
    A single bookable time slot on a specific date.
    Tracks duration and whether the slot is unavailable or already booked.
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
    """"
    A weekday lookup (0=Mon … 6=Sun) with a human-readable name.
    """
    number = models.IntegerField(choices=WEEKDAY_CHOICES, unique=True)
    name   = models.CharField(max_length=9)

    def __str__(self):
        return self.name

class AvailabilityBlock(models.Model):
    """
    A recurring time window over a date range and selected weekdays.
    Used to generate 30-min Availability slots between start_time and end_time.
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
    A user’s appointment occupying one Availability slot for a Treatment.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    availability = models.OneToOneField(
        Availability,
        on_delete=models.PROTECT,
        related_name="booking",
        null=True, blank=True,
        help_text="Which pre-generated slot this booking occupies."
    )

    treatment = models.ForeignKey(
        "services.Treatment",
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name="bookings"
    )

    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
        db_index=True,
    )
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        slot = self.availability
        t = self.treatment or "No treatment"
        if not slot:
            return f"Booking for {self.user} ({t}, no slot)"

        return f"Booking for {self.user} - {t} on {slot.date} from {slot.start_time:%H:%M}"

    def clean(self):
        """
        Don’t allow picking an Availability that already belongs to a *different* booking.
        Allow saving when it's the same row (so admin can change status without errors).
        """
        try:
            other = self.availability.booking
        except Booking.DoesNotExist:
            other = None

        if other and other.pk != self.pk:
            raise ValidationError({"availability": "This time slot is already booked."})
