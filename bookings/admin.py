from django.contrib import admin, messages
from .models import Availability, AvailabilityBlock, Booking, Weekday

@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Weekday model.
    """
    list_display = ('number', 'name')
    ordering     = ('number',)

@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Availability model.
    """
    list_display = ('date', 'start_time', 'end_time', 'unavailable', 'is_booked')
    list_filter  = ('date', 'unavailable', 'is_booked')

@admin.register(AvailabilityBlock)
class AvailabilityBlockAdmin(admin.ModelAdmin):
    """
    Admin configuration for the AvailabilityBlock model.
    """
    list_display      = ('start_date', 'end_date', 'start_time', 'end_time', 'display_days')
    list_filter       = ('start_date', 'end_date')
    filter_horizontal = ('days_of_week',)

    def display_days(self, obj):
        return ", ".join(d.name for d in obj.days_of_week.all())
    display_days.short_description = "Days of week"

@admin.action(description="Confirm selected bookings")
def confirm_bookings(modeladmin, request, queryset):
    updated = queryset.update(status=Booking.Status.APPROVED)
    modeladmin.message_user(request, f"Approved {updated} booking(s).", level=messages.SUCCESS)

@admin.action(description="Cancel selected bookings")
def cancel_bookings(modeladmin, request, queryset):
    updated = queryset.update(status=Booking.Status.CANCELLED)
    modeladmin.message_user(request, f"Cancelled {updated} booking(s).", level=messages.WARNING)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Booking model.
    """
    list_display = ('user', 'availability', 'treatment', 'status', 'created_at')
    list_filter  = ('status', 'created_at', 'treatment')
