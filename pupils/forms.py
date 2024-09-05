from django import forms

from pupils.models import Pupil

from subjects.models import Subjects


class PupilsFilterForm(forms.Form):
    """Класс формы фильтрации учеников"""
    class_counter = forms.IntegerField(
        min_value=5,
        max_value=11,
        label="Класс",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Класс"}
        ),
    )
    skype_only = forms.BooleanField(
        label="Только скайп",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch", "value": 1}
        ),
    )
    is_active = forms.BooleanField(
        label="Только активные",
        required=False,
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "role": "switch", "value": 1}
        ),
    )
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subjects.objects.all(),
        required=False,
        label="Предметы",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )


class CreatePupilForm(forms.ModelForm):
    """Класс формы создания нового ученика"""
    class_counter = forms.IntegerField(
        min_value=5,
        max_value=11,
        label="Класс",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Класс"}
        ),
    )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subjects.objects.all(),
        required=False,
        label="Предметы",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Pupil
        fields = ['name', 'description', 'price_per_hour', 'class_counter', 'skype_only', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            'description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Примечания"}),
            'price_per_hour': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена за час урока"}),
            'skype_only': forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "value": 1}),            
        }


class UpdatePupilForm(forms.ModelForm):
    """Класс формы обновления данных ученика"""
    class_counter = forms.IntegerField(
        min_value=5,
        max_value=11,
        label="Класс",
        required=False,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Класс"}
        ),
    )

    subjects = forms.ModelMultipleChoiceField(
        queryset=Subjects.objects.all(),
        required=False,
        label="Предметы",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Pupil
        fields = ['name', 'description', 'price_per_hour', 'class_counter', 'is_active', 'skype_only', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Имя"}),
            'description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Примечания"}),
            'price_per_hour': forms.NumberInput(attrs={"class": "form-control", "placeholder": "Цена за час урока"}),
            'is_active': forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "value": 1}),          
            'skype_only': forms.CheckboxInput(attrs={"class": "form-check-input", "role": "switch", "value": 1}),          
        }
