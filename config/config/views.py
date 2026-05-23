from django.shortcuts import render
from hotel.models import Hotel

from hotel.models import Hotel
from django.db.models import Q

def home(request):
    query = request.GET.get("q")

    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query)
        )

    return render(request, "home.html", {
        "hotels": hotels,
        "query": query
    })