from django import forms

from lessons.models import Lesson

from pupils.models import Pupil

from subjects.models import Subjects


class LessonsFilterForm(forms.ModelForm):
    """Класс формы фильтрации уроков"""
    class Meta:
        model = Lesson
        fields = ('pupil', 'lesson_datetime', 'subject')
        widgets = {
            'pupil': forms.Select(attrs={'class': 'form-select'}),
            'lesson_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': '08-09-2024 12:00'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        # так как в форме нельзя получить доступ к текущему пользователю, то его нужно явно передать в конструктор в коллекции kwargs
        self.user = kwargs.pop('user', None) 
        super(LessonsFilterForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'
        self.fields['pupil'].required = False

        self.fields['lesson_datetime'].required = False

        self.fields['subject'].empty_label = 'Выбери предмет'
        self.fields['subject'].required = False



class CreateLessonForm(forms.ModelForm):
    """Класс формы создания урока"""
    class Meta:
        model = Lesson
        fields = '__all__'
        widgets = {
            'pupil': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'lesson_datetime': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local', 'placeholder': '08-09-2024 12:00'}),
            'lesson_duration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': 0.5, 'max': 2}),
            'money_recived': forms.NumberInput(attrs={'class': 'form-control'}),

        }
    
    def __init__(self, *args, **kwargs):
        # так как в форме нельзя получить доступ к текущему пользователю, то его нужно явно передать в конструктор в коллекции kwargs
        self.user = kwargs.pop('user', None) 
        super(CreateLessonForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'

        self.fields['subject'].empty_label = 'Выбери предмет'


class UpdateLessonForm(forms.ModelForm):
    """Класс формы обновления данных урока"""
    class Meta:
            model = Lesson
            fields = '__all__'
            widgets = {
                'pupil': forms.Select(attrs={'class': 'form-select'}),
                'subject': forms.Select(attrs={'class': 'form-select'}),
                'lesson_datetime': forms.DateTimeInput(attrs={'class': 'form-control datetime-updater', 
                                                              'type': 'datetime-local', 
                                                              'placeholder': '2024-08-09 12:00'}),
                'lesson_duration': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': 0.5, 'max': 2}),
                'money_recived': forms.NumberInput(attrs={'class': 'form-control'}),
            }
        
    def __init__(self, *args, **kwargs):
        # так как в форме нельзя получить доступ к текущему пользователю, то его нужно явно передать в конструктор в коллекции kwargs
        self.user = kwargs.pop('user', None) 
        super(UpdateLessonForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'

        self.fields['subject'].empty_label = 'Выбери предмет'
