from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from rooms.models import Room

class Booking(models.Model):

    PENDING = 'PENDING'
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'

    BOOKING_STATUS = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (CANCELLED, 'Cancelled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    check_in = models.DateField()
    check_out = models.DateField()

    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS,
        default=PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.check_in >= self.check_out:
            raise ValidationError("Check-out must be after check-in.")

    def __str__(self):
        return f"{self.customer.email} - Room {self.room.id}"