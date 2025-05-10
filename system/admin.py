from django.contrib import admin

from system.models import PatientProfile

@admin.register(PatientProfile)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'date_of_birth')
    list_filter = ('first_name', 'last_name', 'date_of_birth')
    search_fields = ('first_name', 'last_name')
