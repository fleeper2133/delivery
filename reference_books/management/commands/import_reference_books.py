# management/commands/import_reference_books.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reference_books.models import (
    TransportModel,
    PackagingType,
    Service,
    DeliveryStatus,
    CargoType
)

class Command(BaseCommand):
    help = 'Импортирует базовые справочники в базу данных'

    def handle(self, *args, **options):
        self.stdout.write("Начало импорта справочников...")
        
        # 1. Модели транспорта
        transport_models = [
            {"name": "Газель Next", "description": "Грузоподъёмность до 1.5 тонн", "capacity": 1500},
            {"name": "Камаз 6520", "description": "Грузоподъёмность до 20 тонн", "capacity": 20000},
            {"name": "Ford Transit", "description": "Грузоподъёмность до 1 тонны", "capacity": 1000},
            {"name": "Mercedes Sprinter", "description": "Грузоподъёмность до 3 тонн", "capacity": 3000},
        ]
        
        created_count = 0
        for item in transport_models:
            obj, created = TransportModel.objects.get_or_create(
                name=item['name'],
                defaults={
                    'description': item['description'],
                    'capacity': item['capacity']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создана модель транспорта: {obj.name}")
        
        self.stdout.write(f"Импорт моделей транспорта завершен. Создано: {created_count}")

        # 2. Типы упаковки
        packaging_types = [
            {"name": "Пакет до 1 кг", "max_weight": 1, "description": "Полиэтиленовый пакет для лёгких грузов"},
            {"name": "Пакет до 5 кг", "max_weight": 5, "description": "Плотный полиэтиленовый пакет"},
            {"name": "Коробка картонная S", "max_weight": 10, "description": "Малая картонная коробка"},
            {"name": "Коробка картонная M", "max_weight": 20, "description": "Средняя картонная коробка"},
            {"name": "Коробка картонная L", "max_weight": 30, "description": "Большая картонная коробка"},
            {"name": "Паллета", "max_weight": 1000, "description": "Стандартная деревянная паллета"},
            {"name": "Целофан", "max_weight": 3, "description": "Упаковка в целофан"},
        ]
        
        created_count = 0
        for item in packaging_types:
            obj, created = PackagingType.objects.get_or_create(
                name=item['name'],
                defaults={
                    'max_weight': item['max_weight'],
                    'description': item['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создан тип упаковки: {obj.name}")
        
        self.stdout.write(f"Импорт типов упаковки завершен. Создано: {created_count}")

        # 3. Услуги
        services = [
            {"name": "До клиента", "code": "DELIVERY", "price": 300, "description": "Доставка до двери клиента"},
            {"name": "Хрупкий груз", "code": "FRAGILE", "price": 500, "description": "Особые условия перевозки хрупких грузов"},
            {"name": "Мед.товары", "code": "MEDICAL", "price": 700, "description": "Перевозка медицинских товаров с соблюдением условий"},
            {"name": "Срочная доставка", "code": "EXPRESS", "price": 1000, "description": "Доставка в течение 2 часов"},
            {"name": "Подъём на этаж", "code": "LIFTING", "price": 200, "description": "Ручной подъём груза на этаж"},
            {"name": "Страховка", "code": "INSURANCE", "price": 300, "description": "Страхование груза"},
        ]
        
        created_count = 0
        for item in services:
            obj, created = Service.objects.get_or_create(
                code=item['code'],
                defaults={
                    'name': item['name'],
                    'price': item['price'],
                    'description': item['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создана услуга: {obj.name} ({obj.code})")
        
        self.stdout.write(f"Импорт услуг завершен. Создано: {created_count}")

        # 4. Статусы доставки
        statuses = [
            {"name": "В ожидании", "code": "PENDING", "is_active": True, "description": "Заказ создан, ожидает обработки"},
            {"name": "В обработке", "code": "PROCESSING", "is_active": True, "description": "Заказ в процессе обработки"},
            {"name": "Передан в доставку", "code": "DISPATCHED", "is_active": True, "description": "Заказ передан курьеру"},
            {"name": "В пути", "code": "ON_THE_WAY", "is_active": True, "description": "Курьер с заказом в пути к клиенту"},
            {"name": "Доставлено", "code": "DELIVERED", "is_active": False, "description": "Заказ успешно доставлен"},
            {"name": "Отменено", "code": "CANCELED", "is_active": False, "description": "Заказ отменен"},
            {"name": "Возврат", "code": "RETURNED", "is_active": False, "description": "Заказ возвращен"},
        ]
        
        created_count = 0
        for item in statuses:
            obj, created = DeliveryStatus.objects.get_or_create(
                code=item['code'],
                defaults={
                    'name': item['name'],
                    'is_active': item['is_active'],
                    'description': item['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создан статус: {obj.name} ({obj.code})")
        
        self.stdout.write(f"Импорт статусов доставки завершен. Создано: {created_count}")

        # 5. Типы груза (опционально)
        cargo_types = [
            {"name": "Одежда", "requires_special_handling": False, "description": "Текстильные изделия, одежда"},
            {"name": "Электроника", "requires_special_handling": True, "description": "Бытовая и компьютерная техника"},
            {"name": "Мебель", "requires_special_handling": True, "description": "Предметы мебели"},
            {"name": "Продукты", "requires_special_handling": True, "description": "Пищевые продукты (требуют особых условий)"},
            {"name": "Документы", "requires_special_handling": False, "description": "Бумажная документация"},
            {"name": "Медикаменты", "requires_special_handling": True, "description": "Лекарственные средства"},
        ]
        
        created_count = 0
        for item in cargo_types:
            obj, created = CargoType.objects.get_or_create(
                name=item['name'],
                defaults={
                    'requires_special_handling': item['requires_special_handling'],
                    'description': item['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f"Создан тип груза: {obj.name}")
        
        self.stdout.write(f"Импорт типов груза завершен. Создано: {created_count}")

        self.stdout.write(self.style.SUCCESS("Все справочники успешно импортированы!"))