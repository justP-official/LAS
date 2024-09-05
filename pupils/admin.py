from django.contrib import admin

from pupils.models import Pupil

# Register your models here.
@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ('name', 'class_counter', 'is_active', 'skype_only')
    search_fields = ('name', 'class_counter', 'is_active', 'skype_only')
