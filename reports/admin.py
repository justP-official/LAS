from django.contrib import admin

from reports.models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('pupil', 'start_period', 'end_period')
    search_fields = ('pupil', 'start_period', 'end_period')