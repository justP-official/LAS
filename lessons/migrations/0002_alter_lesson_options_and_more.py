# Generated by Django 4.2 on 2024-09-07 09:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pupils', '0004_alter_pupil_options'),
        ('subjects', '0001_initial'),
        ('lessons', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('-lesson_datetime', '-id'), 'verbose_name': 'Урок', 'verbose_name_plural': 'Уроки'},
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='datetime',
            new_name='lesson_datetime',
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_duration',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=3, validators=[django.core.validators.MinValueValidator(1, 'Слишком короткий урок'), django.core.validators.MaxValueValidator(2, 'Слишком долгий урок')], verbose_name='Продолжительность урока'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='pupil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pupil', to='pupils.pupil', verbose_name='Ученик'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject', to='subjects.subjects', verbose_name='Предмет'),
        ),
    ]
