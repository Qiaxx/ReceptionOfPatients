from django.core.management.base import BaseCommand
from system.models import Doctor, AppointmentSlot
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta, time as dt_time

fake = Faker('ru_RU')

SPECIALIZATIONS = [
    'Терапевт', 'Кардиолог', 'Невролог', 'Дерматолог',
    'Офтальмолог', 'Хирург', 'Педиатр', 'Психиатр'
]

class Command(BaseCommand):
    help = 'Создает тестовых врачей и слоты по 30 минут на 20 дней вперед'

    def handle(self, *args, **options):
        Doctor.objects.all().delete()
        AppointmentSlot.objects.all().delete()

        for _ in range(10):
            doctor = Doctor.objects.create(
                first_name=fake.first_name_male(),
                last_name=fake.last_name_male(),
                middle_name=fake.middle_name_male(),
                specialization=random.choice(SPECIALIZATIONS),
                experience_years=random.randint(1, 35),
                photo='doctors/default.jpg'
            )

            # 20 дней вперед, каждый день с 9:00 до 17:00, по 30 минут
            for i in range(20):
                current_date = timezone.now().date() + timedelta(days=i)
                start_hour = 9
                end_hour = 17
                for hour in range(start_hour, end_hour):
                    for minute in (0, 30):
                        slot_time = dt_time(hour=hour, minute=minute)
                        AppointmentSlot.objects.create(
                            doctor=doctor,
                            date=current_date,
                            time=slot_time,
                            duration_minutes=30,
                            is_booked=False
                        )

        self.stdout.write(self.style.SUCCESS('✅ Врачи и 30-минутные слоты успешно созданы.'))