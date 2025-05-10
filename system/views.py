from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import PatientProfileForm
from .models import Region, PatientProfile


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


