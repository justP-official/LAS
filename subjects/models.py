from django.db import models

# Create your models here.
class Subjects(models.Model):
    name = models.CharField(verbose_name='Название предмета', unique=True, max_length=30)
    slug = models.SlugField(verbose_name='URL', unique=True, blank=True, null=True, max_length=50)

    class Meta:
        db_table = 'subject'
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
    
    def __str__(self):
        return self.name
