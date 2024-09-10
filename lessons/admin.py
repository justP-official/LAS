from django.contrib import admin

from lessons.models import Lesson

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('pupil', 'subject', 'lesson_datetime', 'lesson_duration', 'money_recived')
    search_fields = ('pupil', 'subject', 'lesson_datetime', 'lesson_duration', 'money_recived')
