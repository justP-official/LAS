import datetime

from django.db import models
from django.urls import reverse

from pupils.models import Pupil

class Report(models.Model):
    """Модель описания отчёта"""
    pupil = models.ForeignKey(verbose_name='Ученик', to=Pupil, on_delete=models.CASCADE, related_name='reports_pupil')
    start_period = models.DateField(verbose_name='Начало периода', auto_now_add=False)
    end_period = models.DateField(verbose_name='Конец периода', default=datetime.date.today)

    def __str__(self):
        return f"{self.pupil} {self.start_period} {self.end_period}"
    
    def get_absolute_url(self):
        return reverse("reports:read_report", kwargs={"pk": self.pk})
    
    class Meta:
        db_table = 'reports'
        verbose_name = 'Отчёт'
        verbose_name_plural = 'Отчёты'
        ordering = ('-id',)
    
    
