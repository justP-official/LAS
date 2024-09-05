from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from subjects.models import Subjects

from user.models import User


class Pupil(models.Model):
    """Модель описания ученика"""
    name = models.CharField(verbose_name='Имя', max_length=150, unique=True)
    description = models.TextField(verbose_name='Примечание', null=True, blank=True)
    price_per_hour = models.PositiveSmallIntegerField(verbose_name='Цена за час урока', default=0)
    class_counter = models.PositiveSmallIntegerField(verbose_name='Класс', validators=(MinValueValidator(5), MaxValueValidator(11)))
    is_active = models.BooleanField(verbose_name='Активен ли', default=True)
    skype_only = models.BooleanField(verbose_name='Занятия только по Skype', default=False)
    subjects = models.ManyToManyField(to=Subjects, verbose_name='Предметы', blank=True, related_name='subjects')

    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Добавил')

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("pupils:update_pupil", kwargs={"pk": self.pk})
    
    

    class Meta:
        db_table = 'pupils'
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ('-id',)
