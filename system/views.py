from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PatientProfileForm
from .models import Region, PatientProfile, Doctor


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

class AppointmentView(LoginRequiredMixin, View):
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


