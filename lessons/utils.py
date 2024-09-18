from lessons.models import Lesson

def get_lessons_for_period(pupil, start_period, end_period):
    """
    Функция для получения списка уроков с конкретным учеником за определённый период.

    Параметры:
    ----------
    pupil - Ученик, с которым были занятия за определённый период.

    start_period - начало периода.

    end_period - конец периода.

    Возвращаемое значение:
    ----------------------
    lessons - QuerySet с уроками с конкретным учеником за определённый период.
    """
    lessons = Lesson.objects.filter(pupil__id=pupil, lesson_datetime__date__range=[start_period, end_period]).select_related('pupil')

    return lessons
