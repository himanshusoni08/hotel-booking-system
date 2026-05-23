from django.urls import path
from . import views

urlpatterns = [
    # Create a new room for a specific hotel
    path('create/<int:hotel_id>/', views.create_room, name='create_room'),

    # List all rooms for a hotel (owner dashboard)
    path('list/<int:hotel_id>/', views.room_list, name='room_list'),

    # Update a specific room
    path('update/<int:room_id>/', views.update_room, name='update_room'),

    # Delete a specific room
    path('delete/<int:room_id>/', views.delete_room, name='delete_room'),
]