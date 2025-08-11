# bookings/utils.py
from datetime import datetime, timedelta
from .models import Availability

def create_slots_for_date(date, start_time, end_time, slot_minutes=30):
    """
    Generate and persist new Availability slots for a given date.

    This function will slice the time span from `start_time` to `end_time` on
    the specified `date` into consecutive intervals of length `slot_minutes`.
    It skips any intervals that already exist in the database for that date,
    then bulk-creates the remaining slots as unbooked Availability records.

    Parameters:
        date (datetime.date):
            The calendar date for which to generate slots.
        start_time (datetime.time):
            The time on `date` when slot generation should begin.
        end_time (datetime.time):
            The time on `date` when slot generation should end.
        slot_minutes (int, optional):
            Length of each time slot in minutes; defaults to 30.

    Returns:
        list[Availability]:
            The list of newly created Availability instances.
    """
    current = datetime.combine(date, start_time)
    end     = datetime.combine(date, end_time)
    slots   = []

    # gather all existing (start,end) pairs for this date
    existing = {
        (a.start_time, a.end_time)
        for a in Availability.objects.filter(date=date)
    }

    while current + timedelta(minutes=slot_minutes) <= end:
        st = current.time()
        et = (current + timedelta(minutes=slot_minutes)).time()
        if (st, et) not in existing:
            slots.append(Availability(
                date=date,
                start_time=st,
                end_time=et,
                is_booked=False,
            ))
        current += timedelta(minutes=slot_minutes)

    return Availability.objects.bulk_create(slots)
