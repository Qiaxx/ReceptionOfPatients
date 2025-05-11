from django.core.management.base import BaseCommand
from system.models import Doctor, AppointmentSlot
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta

fake = Faker('ru_RU')  # русскоязычные имена

SPECIALIZATIONS = [
    'Терапевт', 'Кардиолог', 'Невролог', 'Дерматолог',
    'Офтальмолог', 'Хирург', 'Педиатр', 'Психиатр'
]

class Command(BaseCommand):
    help = 'Создает тестовых врачей и временные слоты'

    def handle(self, *args, **options):
        Doctor.objects.all().delete()
        AppointmentSlot.objects.all().delete()

        for _ in range(10):  # создадим 10 врачей
            doctor = Doctor.objects.create(
                first_name=fake.first_name_male(),
                last_name=fake.last_name_male(),
                middle_name=fake.middle_name_male(),
                specialization=random.choice(SPECIALIZATIONS),
                experience_years=random.randint(1, 35),
                photo='doctors/default.jpg'  # если нет загрузки, используй дефолт
            )

            # создаём 3 слота на каждый из 3 следующих дней
            for i in range(3):
                date = timezone.now().date() + timedelta(days=i)
                for hour in [10, 12, 14]:
                    AppointmentSlot.objects.create(
                        doctor=doctor,
                        date=date,
                        time=f"{hour}:00"
                    )

        self.stdout.write(self.style.SUCCESS('✅ Врачи и слоты успешно созданы.'))
