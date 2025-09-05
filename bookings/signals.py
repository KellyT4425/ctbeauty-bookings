import datetime
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import AvailabilityBlock
from .utils import create_slots_for_date


@receiver(post_save, sender=AvailabilityBlock)
@receiver(m2m_changed, sender=AvailabilityBlock.days_of_week.through)
def regenerate_block_slots(sender, instance, **kwargs):
    """
    Create/refresh 30-min Availability slots for an AvailabilityBlock.

    On create/update (or weekday changes), iterate dates from start_date to
    end_date; for dates matching the block’s weekdays, call
    create_slots_for_date(start_time→end_time). Existing slots are skipped to
    avoid duplicates.
    """
    weekdays = set(instance.days_of_week.values_list('number', flat=True))

    current = instance.start_date
    while current <= instance.end_date:
        if current.weekday() in weekdays:
            create_slots_for_date(
                date=current,
                start_time=instance.start_time,
                end_time=instance.end_time,
                slot_minutes=30,
            )
        current += datetime.timedelta(days=1)
