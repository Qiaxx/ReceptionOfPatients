from django import forms
from django.core.exceptions import ValidationError

from .models import PatientProfile, Region
import datetime

class PatientProfileForm(forms.ModelForm):
    day = forms.ChoiceField(choices=[(i, i) for i in range(1, 32)], required=True)
    month = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)], required=True)
    year = forms.ChoiceField(choices=[(i, i) for i in range(1900, datetime.date.today().year + 1)], required=True)

    class Meta:
        model = PatientProfile
        fields = ['first_name', 'last_name', 'middle_name', 'gender', 'region']

    def clean(self):
        cleaned_data = super().clean()

        # Получаем значения дня, месяца и года из формы
        day = self.cleaned_data.get('day')
        month = self.cleaned_data.get('month')
        year = self.cleaned_data.get('year')

        # Преобразуем строки в целые числа
        try:
            day = int(day)
            month = int(month)
            year = int(year)
        except ValueError:
            raise ValidationError("Некорректная дата рождения")

        # Создаем объект date
        try:
            cleaned_data['date_of_birth'] = datetime.date(year, month, day)
        except ValueError as e:
            raise ValidationError(f"Ошибка при создании даты: {e}")

        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        instance.user = user
        instance.date_of_birth = self.cleaned_data['date_of_birth']
        if commit:
            instance.save()
        return instance
