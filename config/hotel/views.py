from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hotel
from bookings.models import Booking

# Decorator for owner-only access
from .decorators import owner_required  # make sure you have this decorator


@login_required
def home(request):
    return redirect('home')  # or render homepage


@login_required
@owner_required
def create_hotel(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')  # field is location
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not name or not location or not description:
            messages.error(request, 'All fields except image are required.')
        else:
            hotel = Hotel.objects.create(
                name=name,
                location=location,
                description=description,
                image=image,
                owner=request.user
            )
            messages.success(request, f'Hotel "{hotel.name}" created successfully!')
            return redirect('hotel_list')

    return render(request, 'hotels/create_hotel.html')


@login_required
@owner_required
def hotel_list(request):
    hotels = Hotel.objects.filter(owner=request.user)
    return render(request, 'hotels/hotel_list.html', {"hotels": hotels})


@login_required
@owner_required
def update_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id, owner=request.user)

    if request.method == "POST":
        name = request.POST.get("name")
        location = request.POST.get("location")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if not name or not location or not description:
            messages.error(request, "All fields except image are required.")
        else:
            hotel.name = name
            hotel.location = location
            hotel.description = description
            if image:
                hotel.image = image
            hotel.save()
            messages.success(request, f'Hotel "{hotel.name}" updated successfully!')
            return redirect('hotel_list')

    return render(request, 'hotels/update_hotel.html', {"hotel": hotel})


@login_required
@owner_required
def delete_hotel(request, id):
    hotel = get_object_or_404(Hotel, id=id, owner=request.user)

    if request.method == "POST":
        hotel.delete()
        messages.success(request, f'Hotel "{hotel.name}" deleted successfully!')
        return redirect('hotel_list')

    return render(request, 'hotels/delete_hotel.html', {"hotel": hotel})


@login_required
def hotel_detail(request, id):
    hotel = get_object_or_404(Hotel, id=id)
    rooms = hotel.rooms.all()  # assuming Room model has FK to Hotel

    return render(request, 'hotels/hotel_detail.html', {
        "hotel": hotel,
        "rooms": rooms
    })


@login_required
@owner_required
def owner_bookings(request):
    bookings = Booking.objects.filter(
        room__hotel__owner=request.user
    ).order_by('-created_at')

    return render(request, 'hotels/owner_bookings.html', {
        "bookings": bookings
    })