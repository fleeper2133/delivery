from django.db import models

class TransportModel(models.Model):
    """Модель транспорта"""
    name = models.CharField('Название модели', max_length=100)
    description = models.TextField('Описание', blank=True)
    capacity = models.DecimalField('Грузоподъёмность (кг)', max_digits=8, decimal_places=2)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Модель транспорта'
        verbose_name_plural = 'Модели транспорта'

    def __str__(self):
        return self.name

class PackagingType(models.Model):
    """Тип упаковки"""
    name = models.CharField('Название', max_length=100)
    max_weight = models.DecimalField('Макс. вес (кг)', max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Тип упаковки'
        verbose_name_plural = 'Типы упаковки'

    def __str__(self):
        return self.name

class Service(models.Model):
    """Услуги доставки"""
    name = models.CharField('Название услуги', max_length=100)
    code = models.CharField('Код услуги', max_length=20, unique=True)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f"{self.name} ({self.code})"

class DeliveryStatus(models.Model):
    """Статусы доставки"""
    name = models.CharField('Название статуса', max_length=100)
    code = models.CharField('Код статуса', max_length=20, unique=True)
    is_active = models.BooleanField('Активный статус', default=True)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Статус доставки'
        verbose_name_plural = 'Статусы доставки'

    def __str__(self):
        return self.name

class CargoType(models.Model):
    """Типы груза (опционально)"""
    name = models.CharField('Тип груза', max_length=100)
    requires_special_handling = models.BooleanField('Требует спецобработки', default=False)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Тип груза'
        verbose_name_plural = 'Типы груза'

    def __str__(self):
        return self.name
