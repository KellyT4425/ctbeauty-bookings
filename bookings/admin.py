# bookings/admin.py
from django.contrib import admin
from .models import Availability, AvailabilityBlock, Booking, Weekday

@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Weekday model.

    - list_display: show the 'number' (0–6) and 'name' (e.g. Monday) columns in the changelist.
    - ordering: sort the changelist by the 'number' field.
    """
    list_display = ('number', 'name')
    ordering     = ('number',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Availability model.

    - list_display: show date, start_time, end_time, unavailable flag, and is_booked flag.
    - list_filter: add sidebar filters for date, unavailable, and is_booked.
    """
    list_display = ('date', 'start_time', 'end_time', 'unavailable', 'is_booked')
    list_filter  = ('date', 'unavailable', 'is_booked')

@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AvailabilityBlock model.

    - list_display: show start_date, end_date, start_time, end_time, and a custom
      `display_days` showing the selected weekdays.
    - list_filter: add sidebar filters for start_date and end_date.
    - filter_horizontal: use a horizontal widget for the days_of_week many-to-many field.
    """
    list_display      = ('start_date', 'end_date', 'start_time', 'end_time', 'display_days')
    list_filter       = ('start_date', 'end_date')
    filter_horizontal = ('days_of_week',)

    def display_days(self, obj):
        return ", ".join(d.name for d in obj.days_of_week.all())
    display_days.short_description = "Days of week"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.

    - list_display: show the user, linked availability slot, treatment, status, and creation timestamp.
    - list_filter: add sidebar filters for status, created_at date, and treatment.
    """
    list_display = ('user', 'availability', 'treatment', 'status', 'created_at')
    list_filter  = ('status', 'created_at', 'treatment')
