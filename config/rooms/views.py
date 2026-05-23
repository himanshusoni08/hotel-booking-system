from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from hotel.models import Hotel
from .models import Room
from hotel.decorators import owner_required

@login_required
@owner_required
def create_room(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    context = {"hotel": hotel}

    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_type = request.POST.get("room_type")
        price = request.POST.get("price")

        if not room_number or not room_type or not price:
            context["error"] = "All fields are required."
        else:
            Room.objects.create(
                hotel=hotel,
                room_number=room_number,
                room_type=room_type,
                price=price
            )
            context["success"] = f"Room {room_number} created successfully!"

    return render(request, "rooms/create_room.html", context)


@login_required
@owner_required
def room_list(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id, owner=request.user)
    rooms = hotel.rooms.all()
    return render(request, "rooms/room_list.html", {"hotel": hotel, "rooms": rooms})


@login_required
@owner_required
def update_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, hotel__owner=request.user)
    context = {"room": room}

    if request.method == "POST":
        room_number = request.POST.get("room_number")
        room_type = request.POST.get("room_type")
        price = request.POST.get("price")
        is_available = request.POST.get("is_available") == "on"

        if not room_number or not room_type or not price:
            context["error"] = "All fields are required."
        else:
            room.room_number = room_number
            room.room_type = room_type
            room.price = price
            room.is_available = is_available
            room.save()
            context["success"] = "Room updated successfully!"

    return render(request, "rooms/update_room.html", context)


@login_required
@owner_required
def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id, hotel__owner=request.user)

    if request.method == "POST":
        room.delete()
        return redirect("room_list", hotel_id=room.hotel.id)

    return render(request, "rooms/delete_room.html", {"room": room})