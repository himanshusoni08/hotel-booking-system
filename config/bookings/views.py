from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking
from rooms.models import Room
from datetime import datetime

@login_required
def create_booking(request, room_id):

    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")

        try:
            check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
            check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        except:
            messages.error(request, "Invalid date format.")
            return redirect("create_booking", room_id=room.id)

        # Date validation
        if check_in >= check_out:
            messages.error(request, "Check-out must be after check-in.")
            return redirect("create_booking", room_id=room.id)

        if check_in < timezone.now().date():
            messages.error(request, "Check-in date cannot be in the past.")
            return redirect("create_booking", room_id=room.id)

        # Prevent double booking
        overlapping = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in,
            status=Booking.CONFIRMED
        )

        if overlapping.exists():
            messages.error(request, "Room already booked for selected dates.")
            return redirect("create_booking", room_id=room.id)

        # Calculate total price
        total_days = (check_out - check_in).days
        total_price = total_days * room.price

        Booking.objects.create(
            customer=request.user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status=Booking.PENDING
        )

        messages.success(request, "Booking request created successfully!")
        return redirect("my_bookings")

    return render(request, "bookings/create_booking.html", {"room": room})


@login_required
def my_bookings(request):

    if request.user.role == "CUSTOMER":
        bookings = Booking.objects.filter(customer=request.user).order_by("-created_at")
    else:
        bookings = Booking.objects.filter(room__hotel__owner=request.user).order_by("-created_at")

    return render(request, "bookings/my_bookings.html", {"bookings": bookings})