from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Booking, Availability
from .forms import BookingForm


@login_required
def make_booking(request):
    """
    Display and process the booking form.
    - GET: empty form (optionally pre-filtered by category).
    - POST: create a booking, attach user, and mark slot as booked.
    """
    category_id = request.POST.get('category') or request.GET.get('category')

    if request.method == 'POST':
        form = BookingForm(request.POST, category_id=category_id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user

            # mark selected slot as taken
            if booking.availability:
                slot = booking.availability
                slot.is_booked = True
                slot.save()

            booking.save()
            return redirect('bookings:list')
    else:
        form = BookingForm(category_id=category_id)

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'category_id': category_id
    })


# EDIT EXISTING BOOKING
@login_required
def edit_booking(request, pk):
    """
    Edit an existing booking owned by the user.
    Allows re-selecting treatment, slot, or notes.
    """
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    category_id = request.POST.get('category') or booking.treatment.category.pk

    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking, category_id=category_id)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            return redirect('bookings:list')
    else:
        form = BookingForm(instance=booking, category_id=category_id)

    return render(request, 'bookings/booking_form.html', {
        'form': form,
        'category_id': category_id,
        'edit': True
    })


# LIST BOOKINGS
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user).select_related('availability', 'treatment')
    return render(request, 'bookings/booking_list.html', {
        'bookings': bookings
    })



# VIEW SINGLE BOOKING
@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking
    })


# CANCEL BOOKING
@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)

    if request.method == 'POST':
        if booking.availability:
            slot = booking.availability
            slot.is_booked = False
            slot.save()
        booking.delete()
        return redirect('bookings:list')

    return render(request, 'bookings/booking_confirm_cancel.html', {'booking': booking})



"""
B. Bookings app views
1. make_booking
URL: /bookings/make/

Access: only for logged-in users (@login_required).

Purpose: let the user pick an open time slot and create a booking.

Steps:

On GET:

Query Availability for all slots where unavailable=False, is_booked=False, and date ≥ today.

Instantiate your BookingForm, replacing its “availability” queryset with that list.

Render the form template with { "form": form }.

On POST:

Bind BookingForm(request.POST).

If valid:

Call form.save(commit=False), attach form.instance.user = request.user, then form.save().

Mark form.instance.availability.is_booked = True and save that slot.

Redirect to a confirmation page or to My Bookings.

If invalid: re-render the form with errors.

2. my_bookings
URL: /bookings/my/

Access: logged-in only.

Purpose: list all bookings made by the current user.

Steps:

Query Booking.objects.filter(user=request.user).order_by('-created_at').

Pass them into template as { "bookings": bookings }.

Template loops over each and displays the slot’s date/time, service name, status, and maybe a “Cancel” link.

3. cancel_booking
URL: /bookings/cancel/<pk>/

Access: logged-in only.

Purpose: allow a user to cancel one of their bookings.

Steps:

Lookup the Booking by pk and ensure booking.user == request.user (403 otherwise).

Set booking.status = 'CANCELLED' (or delete it) and save.

Also mark booking.availability.is_booked = False so the slot re-opens.

Redirect back to My Bookings with a success message.

C. Templates you’ll need
services/treatment_list.html

services/treatment_detail.html

bookings/make.html (form)

bookings/my.html (list)

Optionally a bookings/confirm.html for a success page

All should extend your base.html and live under templates/services/ or templates/bookings/.

D. Forms


"""
