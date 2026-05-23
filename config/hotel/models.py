from django.db import models
from django.conf import settings

class Hotel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hotels'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hotel_images/', blank=True, null=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name