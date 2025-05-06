from django.db import models

# models.py
from django.db import models
from django.contrib.auth.models import User



class Delivery(models.Model):
    """Основная модель доставки"""
    tracking_number = models.CharField('Трек-номер', max_length=50, unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='deliveries', verbose_name='Клиент')
    transport = models.ForeignKey('reference_books.TransportModel', on_delete=models.PROTECT, verbose_name='Модель транспорта')
    transport_number = models.CharField('Номер транспорта', max_length=20)
    packaging_type = models.ForeignKey('reference_books.PackagingType', on_delete=models.PROTECT, verbose_name='Тип упаковки')
    cargo_type = models.ForeignKey('reference_books.CargoType', on_delete=models.PROTECT, verbose_name='Тип груза', null=True, blank=True)
    weight = models.DecimalField('Вес (кг)', max_digits=8, decimal_places=2)
    volume = models.DecimalField('Объём (м³)', max_digits=8, decimal_places=3, null=True, blank=True)
    status = models.ForeignKey('reference_books.DeliveryStatus', on_delete=models.PROTECT, verbose_name='Статус')
    services = models.ManyToManyField('reference_books.Service', verbose_name='Услуги', blank=True)
    pickup_address = models.TextField('Адрес забора')
    delivery_address = models.TextField('Адрес доставки')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    scheduled_pickup = models.DateTimeField('Запланирован забор', null=True, blank=True)
    scheduled_delivery = models.DateTimeField('Запланирована доставка', null=True, blank=True)
    actual_pickup = models.DateTimeField('Фактический забор', null=True, blank=True)
    actual_delivery = models.DateTimeField('Фактическая доставка', null=True, blank=True)
    notes = models.TextField('Примечания', blank=True)
    distance_km = models.DecimalField('Расстояние (км)', max_digits=8, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField('Итоговая стоимость', max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'
        ordering = ['-created_at']

    def __str__(self):
        return f"Доставка #{self.tracking_number} ({self.status})"

    def calculate_total_price(self):
        """Рассчитывает общую стоимость доставки"""
        base_price = 100  # Базовая цена, можно заменить на логику из модели
        services_price = sum(service.price for service in self.services.all())
        return base_price + services_price

class DeliveryMedia(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='delivery_media/')
    file_type = models.CharField(max_length=50)  # image/jpeg, application/pdf и т.д.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Медиафайл доставки'
        verbose_name_plural = 'Медиафайлы доставки'

    def __str__(self):
        return f"Медиафайл #{self.id} для доставки {self.delivery.tracking_number}"