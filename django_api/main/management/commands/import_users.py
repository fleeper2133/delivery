# management/commands/import_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Создает тестовых пользователей (admin и test) если они не существуют'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # 1. Создаем суперпользователя admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin',
                first_name='Администратор',
                last_name='Системы'
            )
            self.stdout.write(self.style.SUCCESS('Создан суперпользователь: admin (password: admin)'))
        else:
            self.stdout.write('Суперпользователь admin уже существует')

        # 2. Создаем обычного пользователя test
        if not User.objects.filter(username='test').exists():
            User.objects.create_user(
                username='test',
                email='test@example.com',
                password='12345',
                first_name='Иван',
                last_name='Петров',
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS('Создан пользователь: test (password: 12345)'))
        else:
            self.stdout.write('Пользователь test уже существует')

        self.stdout.write(self.style.SUCCESS('Проверка пользователей завершена'))