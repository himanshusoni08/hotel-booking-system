from django.contrib import admin
from .models import Hotel

# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'created_at')
    list_filter = ('location', 'created_at')
    search_fields = ('name', 'location')
    ordering = ('-created_at',)


admin.site.register(Hotel, HotelAdmin)