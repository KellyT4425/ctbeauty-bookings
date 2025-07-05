import datetime
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import AvailabilityBlock
from .utils import create_slots_for_date

@receiver(post_save, sender=AvailabilityBlock)
@receiver(m2m_changed, sender=AvailabilityBlock.days_of_week.through)
def regenerate_block_slots(sender, instance, **kwargs):
    """
    Any time a block is saved or its weekdays change,
    walk the date range and generate slots (duplicates skipped).
    """
    # pull out the weekday numbers the admin selected
    weekdays = set(instance.days_of_week.values_list('number', flat=True))

    current = instance.start_date
    while current <= instance.end_date:
        if current.weekday() in weekdays:
            create_slots_for_date(
                date=current,
                start_time=instance.start_time,
                end_time=instance.end_time,
                slot_minutes=30,  # or 15 if you prefer
            )
        current += datetime.timedelta(days=1)
