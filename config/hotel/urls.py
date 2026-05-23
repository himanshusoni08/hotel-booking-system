from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_hotel, name='create_hotel'),
    path('list/', views.hotel_list, name='hotel_list'),  # explicit URL is safer
    path('update/<int:id>/', views.update_hotel, name='update_hotel'),
    path('delete/<int:id>/', views.delete_hotel, name='delete_hotel'),
    path('detail/<int:id>/', views.hotel_detail, name='hotel_detail'),  # clearer than just <int:id>/
    path('bookings/', views.owner_bookings, name='owner_bookings'),
]