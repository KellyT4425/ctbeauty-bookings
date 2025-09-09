from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking
from .forms import BookingForm
from django.contrib import messages


@login_required
def make_booking(request):
    """
    Show and process the booking form.

    GET: render form (category preselected via ?category=).
    POST: validate, attach user, mark chosen slot booked, save, flash success,
    then redirect to `bookings:list`; on errors, re-render with messages.
    """
    category_id = request.POST.get("category") or request.GET.get("category")
    treatment_id = request.POST.get(
        "treatment") or request.GET.get("treatment")

    if request.method == "POST":
        form = BookingForm(request.POST or None,
                           category_id=category_id,
                           treatment_id=treatment_id,)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            if booking.availability:
                slot = booking.availability
                slot.is_booked = True
                slot.save()
            booking.save()
            messages.success(
                request,
                f"Booking confirmed for {booking.treatment.name} on "
                f"{booking.availability.date:%b %d, %Y} at "
                f"{booking.availability.start_time:%H:%M}."
            )
            return redirect("bookings:list")
        else:
            messages.error(request, "Please fix the errors below.")

    else:
        form = BookingForm(request.GET, category_id=category_id)

    return render(request, "bookings/booking_form.html", {
        "form": form,
        "category_id": category_id,
    })

# EDIT EXISTING BOOKING


@login_required
def edit_booking(request, pk):
    """
    Let a user change only the booking's Availability.

    Loads the booking, disables Category/Treatment/Notes via the form flag,
    toggles old/new slot `is_booked` if the time changes, flashes success,
    then redirects to `bookings:list`.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    category_id = booking.treatment.category_id
    old_slot = booking.availability

    form = BookingForm(
        request.POST or None,
        instance=booking,
        category_id=category_id,
        edit_availability=True,
    )

    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        updated.user = request.user
        new_slot = form.cleaned_data.get("availability")

        if old_slot and new_slot and old_slot != new_slot:
            old_slot.is_booked = False
            old_slot.save(update_fields=["is_booked"])
            if not new_slot.is_booked:
                new_slot.is_booked = True
                new_slot.save(update_fields=["is_booked"])

        updated.save()
        messages.success(request, "Booking time updated.")
        return redirect("bookings:list")

    return render(request, "bookings/booking_form.html", {
        "form": form,
        "edit": True,
        "category_id": category_id,
    })


# LIST BOOKINGS
@login_required
def my_bookings(request):
    """
    List the current user's bookings.

    Uses `select_related('availability','treatment')` and renders
    `bookings/booking_list.html`.
    """
    bookings = Booking.objects.filter(
        user=request.user).select_related('availability', 'treatment')
    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings
    })


# VIEW SINGLE BOOKING
@login_required
def booking_detail(request, pk):
    """
    Show a single booking owned by the user (404 if not found/not owned).

    Renders `bookings/booking_detail.html`.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


# CANCEL BOOKING
@login_required
def cancel_booking(request, pk):
    """
    Cancel a booking and free its slot.

    GET: confirm page. POST: set slot `is_booked=False`, delete booking,
    flash success, redirect to `bookings:list`.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        # free slot, then delete
        if booking.availability:
            slot = booking.availability
            slot.is_booked = False
            slot.save(update_fields=["is_booked"])
        booking.delete()
        messages.success(request, "Your booking has been cancelled.")
        return redirect('bookings:list')

    return render(request,
                  'bookings/booking_confirm_cancel.html',
                  {'booking': booking})
