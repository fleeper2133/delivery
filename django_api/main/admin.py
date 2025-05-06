# admin.py
from django.contrib import admin
from .models import Delivery, DeliveryMedia

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'customer', 'status', 'scheduled_delivery', 'created_at')
    list_filter = ('status', 'created_at', 'transport')
    search_fields = ('tracking_number', 'customer__username', 'pickup_address', 'delivery_address')
    raw_id_fields = ('customer',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    filter_horizontal = ('services',)

admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(DeliveryMedia)
