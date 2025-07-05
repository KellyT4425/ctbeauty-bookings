# bookings/admin.py
from django.contrib import admin
from .models import Availability, AvailabilityBlock, Booking, Weekday

@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
    ordering     = ('number',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'unavailable', 'is_booked')
    list_filter  = ('date', 'unavailable', 'is_booked')

@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    list_display      = ('start_date', 'end_date', 'start_time', 'end_time', 'display_days')
    list_filter       = ('start_date', 'end_date')
    filter_horizontal = ('days_of_week',)

    def display_days(self, obj):
        return ", ".join(d.name for d in obj.days_of_week.all())
    display_days.short_description = "Days of week"

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'availability', 'treatment', 'status', 'created_at')
    list_filter  = ('status', 'created_at', 'treatment')
