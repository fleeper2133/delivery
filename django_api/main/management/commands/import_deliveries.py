from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
import random
from datetime import datetime, timedelta
from reference_books.models import (
    TransportModel,
    PackagingType,
    Service,
    DeliveryStatus,
    CargoType
)
from main.models import Delivery

class Command(BaseCommand):
    help = 'Импортирует тестовые данные доставок (только если их еще нет)'

    def handle(self, *args, **options):
        self.stdout.write("Проверка и импорт тестовых доставок...")
        
        # Проверяем, есть ли уже тестовые доставки
        if Delivery.objects.exists():
            self.stdout.write(self.style.WARNING("Тестовые доставки уже существуют, импорт пропущен."))
            return

        fake = Faker('ru_RU')
        User = get_user_model()
        
        # Получаем все справочники
        transport_models = list(TransportModel.objects.all())
        packaging_types = list(PackagingType.objects.all())
        services = list(Service.objects.all())
        statuses = list(DeliveryStatus.objects.all())
        cargo_types = list(CargoType.objects.all())
        
        # Проверяем и создаем тестового пользователя
        try:
            customer = User.objects.get(username='test')
        except User.DoesNotExist:
            customer = User.objects.create_user(
                username='test',
                email='customer@example.com',
                password='12345',
                first_name='Иван',
                last_name='Петров'
            )
            self.stdout.write("Создан тестовый пользователь: test (password: 12345)")

        # Создаем группы доставок (3-10 доставок в одной группе)
        delivery_groups = []
        
        # 1. Группировка по датам (создаем 5-7 групп дат)
        date_groups = []
        for _ in range(random.randint(5, 7)):
            base_date = fake.date_time_between(start_date='-30d', end_date='now')
            pickup_days = random.randint(1, 3)
            delivery_days = random.randint(3, 7)
            
            date_groups.append({
                'base_date': base_date,
                'pickup_days': pickup_days,
                'delivery_days': delivery_days
            })
        
        # 2. Группировка по типам доставки (услуги + тип груза)
        delivery_types = []
        for _ in range(3):  # 3 разных типа доставки
            main_services = random.sample(services, random.randint(1, 2))
            extra_services = random.sample(
                [s for s in services if s not in main_services], 
                random.randint(0, 2)
            )
            selected_services = main_services + extra_services
            cargo = random.choice(cargo_types) if random.choice([True, False]) else None
            
            delivery_types.append({
                'services': selected_services,
                'cargo_type': cargo,
                'packaging': random.choice(packaging_types),
                'transport': random.choice(transport_models)
            })
        
        # Создаем доставки, объединяя группы
        delivery_id = 1
        created_count = 0
        for date_group in date_groups:
            for delivery_type in delivery_types:
                num_deliveries = random.randint(3, 10)
                
                for i in range(num_deliveries):
                    if created_count >= 20:  # Ограничение в 20 доставок
                        break
                    
                    date_variation = timedelta(days=random.randint(0, 2), hours=random.randint(0, 12))
                    
                    created_at = date_group['base_date'] + date_variation
                    scheduled_pickup = created_at + timedelta(days=date_group['pickup_days'])
                    scheduled_delivery = created_at + timedelta(days=date_group['delivery_days'])
                    
                    if random.choice([True, False]):
                        actual_pickup = scheduled_pickup + timedelta(hours=random.randint(0, 12))
                        actual_delivery = scheduled_delivery + timedelta(hours=random.randint(0, 12))
                        status = DeliveryStatus.objects.get(code='DELIVERED')
                    else:
                        actual_pickup = None
                        actual_delivery = None
                        status = random.choice([s for s in statuses if s.is_active])
                    
                    weight = round(random.uniform(0.1, 100), 2)
                    volume = round(random.uniform(0.01, 5), 3) if random.choice([True, False]) else None
                    distance = round(random.uniform(1, 500), 2) if random.choice([True, False]) else None
                    
                    # Рассчитываем общую стоимость
                    total_price = round(random.uniform(300, 5000), 2)
                    
                    delivery = Delivery.objects.create(
                        tracking_number=f"TRK{100000 + delivery_id}",
                        customer=customer,
                        transport=delivery_type['transport'],
                        transport_number=fake.license_plate(),
                        packaging_type=delivery_type['packaging'],
                        cargo_type=delivery_type['cargo_type'],
                        weight=weight,
                        volume=volume,
                        status=status,
                        pickup_address=fake.address(),
                        delivery_address=fake.address(),
                        created_at=created_at,
                        updated_at=created_at + timedelta(hours=random.randint(1, 24)),
                        scheduled_pickup=scheduled_pickup,
                        scheduled_delivery=scheduled_delivery,
                        actual_pickup=actual_pickup,
                        actual_delivery=actual_delivery,
                        notes=f"Доставка #{i+1} в группе" if random.choice([True, False]) else '',
                        distance_km=distance,
                        total_price=total_price
                    )
                    
                    delivery.services.set(delivery_type['services'])
                    created_count += 1
                    delivery_id += 1
                    self.stdout.write(f"Создана доставка #{created_count}: {delivery.tracking_number}")

        self.stdout.write(self.style.SUCCESS(f"Успешно создано {created_count} тестовых доставок!"))