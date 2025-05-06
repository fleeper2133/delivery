from django.contrib import admin
from .models import Service, TransportModel, PackagingType, DeliveryStatus, CargoType


class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "price")
    search_fields = ("name", "code")


class TransportModelAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity")
    search_fields = ("name",)


class PackagingTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "max_weight")
    search_fields = ("name",)


class DeliveryStatusAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "code")


class CargoTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "requires_special_handling")
    list_filter = ("requires_special_handling",)
    search_fields = ("name",)


# Регистрация моделей
admin.site.register(TransportModel, TransportModelAdmin)
admin.site.register(PackagingType, PackagingTypeAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(DeliveryStatus, DeliveryStatusAdmin)
admin.site.register(CargoType, CargoTypeAdmin)
