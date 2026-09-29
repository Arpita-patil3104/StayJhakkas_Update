from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from properties.models import Property, Bed

from .forms import BookingForm
from .models import Booking


# ============================================================
# CREATE BOOKING
# ============================================================

@login_required
def create_booking(request, property_id):

    # Get the selected PG using its ID
    property_obj = get_object_or_404(
        Property,
        id=property_id,
        is_active=True,
        is_approved=True
    )

    # Get only vacant beds
    available_beds = Bed.objects.filter(
        room__pg=property_obj,
        room__is_active=True,
        status="vacant"
    ).select_related("room")

    # No beds available
    if not available_beds.exists():
        return render(
            request,
            "bookings/booking_form.html",
            {
                "property": property_obj,
                "form": None,
                "no_beds": True,
            }
        )

    # ========================================================
    # POST - CREATE BOOKING
    # ========================================================

    if request.method == "POST":

        form = BookingForm(
            request.POST,
            property_obj=property_obj
        )

        if form.is_valid():

            bed = form.cleaned_data.get("bed")

            # Make sure a bed was selected
            if bed is None:

                form.add_error(
                    "bed",
                    "Please select an available bed."
                )

            # Make sure bed is still vacant
            elif bed.status != "vacant":

                form.add_error(
                    "bed",
                    "This bed is no longer available. Please select another bed."
                )

            else:

                # Create booking + reserve bed safely
                with transaction.atomic():

                    booking = form.save(commit=False)

                    booking.tenant = request.user
                    booking.property = property_obj

                    # Take current PG rent/deposit
                    booking.monthly_rent = property_obj.monthly_rent
                    booking.security_deposit = property_obj.security_deposit

                    # Selected room and bed
                    booking.room = bed.room
                    booking.bed = bed

                    # New request
                    booking.status = "pending"

                    booking.save()

                    # Reserve bed
                    bed.status = "reserved"
                    bed.save(update_fields=["status"])

                # Go to booking details
                return redirect(
                    "booking_detail",
                    booking_id=booking.id
                )

    else:

        form = BookingForm(
            property_obj=property_obj
        )

    return render(
        request,
        "bookings/booking_form.html",
        {
            "property": property_obj,
            "form": form,
            "no_beds": False,
        }
    )


# ============================================================
# MY BOOKINGS
# ============================================================

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(
        tenant=request.user
    ).select_related(
        "property",
        "room",
        "bed"
    )

    return render(
        request,
        "bookings/my_bookings.html",
        {
            "bookings": bookings
        }
    )


# ============================================================
# BOOKING DETAIL
# ============================================================

@login_required
def booking_detail(request, booking_id):

    booking = get_object_or_404(
        Booking.objects.select_related(
            "tenant",
            "property",
            "room",
            "bed"
        ),
        id=booking_id
    )

    # Tenant can view own booking
    # Owner can view booking of their PG
    if (
        booking.tenant != request.user
        and booking.property.owner != request.user
    ):
        return redirect("home")

    return render(
        request,
        "bookings/booking_detail.html",
        {
            "booking": booking
        }
    )


# ============================================================
# OWNER BOOKING REQUESTS
# ============================================================

@login_required
def owner_bookings(request):

    bookings = Booking.objects.filter(
        property__owner=request.user
    ).select_related(
        "tenant",
        "property",
        "room",
        "bed"
    )

    return render(
        request,
        "bookings/owner_bookings.html",
        {
            "bookings": bookings
        }
    )


# ============================================================
# APPROVE BOOKING
# ============================================================

@login_required
def approve_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        property__owner=request.user
    )

    if request.method == "POST":

        booking.status = "approved"

        booking.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        # Approved booking → bed becomes occupied
        if booking.bed:

            booking.bed.status = "occupied"

            booking.bed.save(
                update_fields=["status"]
            )

        return redirect("owner_bookings")

    return redirect("owner_bookings")


# ============================================================
# REJECT BOOKING
# ============================================================

@login_required
def reject_booking(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        property__owner=request.user
    )

    if request.method == "POST":

        booking.status = "rejected"

        booking.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )

        # Rejected booking → release bed
        if booking.bed:

            booking.bed.status = "vacant"

            booking.bed.save(
                update_fields=["status"]
            )

        return redirect("owner_bookings")

    return redirect("owner_bookings")