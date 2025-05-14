from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PatientProfileForm
from .models import Region, PatientProfile, Doctor, AppointmentSlot, Appointment


@method_decorator(login_required, name='dispatch')
class RegisterPatientProfileView(View):
    model = PatientProfile
    template_name = 'system/personal_user_data.html'
    success_url = 'users:login'

    def get_context_data(self, **kwargs):
        current_year = timezone.now().year
        context = {
            'form': kwargs.get('form'),
            'regions': Region.objects.all(),
            'days': range(1, 32),
            'months': range(1, 13),
            'years': range(1900, current_year + 1),
        }
        return context

    def get(self, request):
        form = PatientProfileForm()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request):
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect(self.success_url)
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

class ChooseView(View):
    template_name = 'system/consultation.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class DoctorsView(LoginRequiredMixin, View):
    template_name = 'system/appointment.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        selected_specialty = request.GET.get('specialty', '')
        sort_by = request.GET.get('sort', '')

        doctors = Doctor.objects.all()

        if selected_specialty:
            doctors = doctors.filter(specialization=selected_specialty)

        if search_query:
            doctors = doctors.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(middle_name__icontains=search_query)
            )

        if sort_by == 'date':
            # Это временно — сортировка по id, т.к. слотов нет в контексте
            doctors = doctors.order_by('id')

        specialties = Doctor.objects.values_list('specialization', flat=True).distinct()
        patient = PatientProfile.objects.get(user=request.user)

        context = {
            'doctors': doctors,
            'specialties': specialties,
            'selected_specialty': selected_specialty,
            'search_query': search_query,
            'sort_by': sort_by,
            'patient': patient,
        }

        return render(request, self.template_name, context)


class AppointmentView(View):

    def get(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        return render(request, 'system/appointment_calendar.html', {'doctor': doctor})

    def post(self, request, doctor_id):
        doctor = get_object_or_404(Doctor, id=doctor_id)
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')

        if not date_str or not time_str:
            return render(request, 'system/appointment_calendar.html', {
                'doctor': doctor,
                'error': 'Пожалуйста, выберите дату и время.'
            })

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            return render(request, 'system/appointment_calendar.html', {
                'doctor': doctor,
                'error': 'Неверный формат даты или времени.'
            })

        slot = AppointmentSlot.objects.filter(
            doctor=doctor,
            date=date,
            time=time,
            is_booked=False
        ).first()

        if not slot:
            return render(request, 'system/appointment_calendar.html', {
                'doctor': doctor,
                'error': 'Выбранный слот уже занят или не существует.'
            })

        if not request.user.is_authenticated:
            return redirect('users:login')

        try:
            patient_profile = request.user.patientprofile
        except PatientProfile.DoesNotExist:
            return render(request, 'system/appointment_calendar.html', {
                'doctor': doctor,
                'error': 'Ваш профиль пациента не найден.'
            })

            # Проверка: нет ли уже записи на этот день
        existing = Appointment.objects.filter(
            patient=patient_profile,
            slot__date=date
        ).exists()

        if existing:
            return render(request, 'system/appointment_calendar.html', {
                'doctor': doctor,
                'error': 'У вас уже есть запись на этот день.'
            })

        # Создание записи
        Appointment.objects.create(patient=patient_profile, slot=slot)
        slot.is_booked = True
        slot.save()

        return redirect('system:choose')  # Замените на ваш маршрут успешной записи


def get_free_slots(request):
    date_str = request.GET.get('date')
    doctor_id = request.GET.get('doctor_id')

    if not date_str or not doctor_id:
        return JsonResponse({'slots': []})

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'slots': []})

    slots = AppointmentSlot.objects.filter(
        doctor_id=doctor_id,
        date=date,
        is_booked=False
    ).order_by('time')

    slot_times = [slot.time.strftime('%H:%M') for slot in slots]

    return JsonResponse({'slots': slot_times})