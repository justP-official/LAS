from django.contrib import admin

from subjects.models import Subjects

# Register your models here.
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['name',]}
    list_display = ('name',)
