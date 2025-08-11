import datetime
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import AvailabilityBlock
from .utils import create_slots_for_date

@receiver(post_save, sender=AvailabilityBlock)
@receiver(m2m_changed, sender=AvailabilityBlock.days_of_week.through)
def regenerate_block_slots(sender, instance, **kwargs):
    """
    Signal handler for AvailabilityBlock changes.

    Whenever an AvailabilityBlock is created, updated, or its associated
    weekdays are modified, this function will:

    1. Determine which weekdays (0=Monday…6=Sunday) the block applies to.
    2. Iterate each date from `instance.start_date` through `instance.end_date`.
    3. For each date that falls on one of the selected weekdays, call
       `create_slots_for_date()` to generate 30-minute Availability slots
       between `instance.start_time` and `instance.end_time`.
    4. Skip any slots that already exist, avoiding duplicates.

    Parameters:
        sender (type): The model class sending the signal (AvailabilityBlock).
        instance (AvailabilityBlock): The block instance that was saved or modified.
        **kwargs: Additional keyword arguments provided by Django’s signal.

    Returns:
        None
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
