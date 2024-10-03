import locale

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

from pupils.models import Pupil

from subjects.models import Subjects


locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8')) # установка локали для отображения даты на русском


class LessonQuerySet(models.QuerySet):
    def total_money(self):
        return sum(lesson.money_recived for lesson in self)


class Lesson(models.Model):
    pupil = models.ForeignKey(verbose_name='Ученик',
                              to=Pupil,
                              on_delete=models.CASCADE,
                              related_name='pupil'
                              )
    
    subject = models.ForeignKey(verbose_name='Предмет',
                                to=Subjects,
                                on_delete=models.CASCADE,
                                related_name='subject'
                                )
    
    lesson_datetime = models.DateTimeField(verbose_name='Дата проведения урока',
                                    auto_now_add=False,
                                    unique=True
                                    )
    
    lesson_duration = models.DecimalField(verbose_name='Продолжительность урока', 
                                          decimal_places=2, 
                                          max_digits=3,
                                          default=1,
                                          validators=(MinValueValidator(1, 'Слишком короткий урок'),
                                                      MaxValueValidator(2, 'Слишком долгий урок'))
                                        )
    
    money_recived = models.DecimalField(verbose_name='Денег заработано', 
                                        decimal_places=2, 
                                        max_digits=7,
                                        default=0
                                        )
    
    objects = LessonQuerySet.as_manager()
    
    def __str__(self):
        return f"Урок с учеником: {self.pupil}; По предмету: {self.subject}; За {self.lesson_datetime.strftime('%d %b %Y %H:%M')}"
    
    def get_absolute_url(self):
        return reverse("lessons:update_lesson", kwargs={"pk": self.pk})
    

    class Meta:
        db_table = 'lessons'
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('-lesson_datetime', '-id')
    
