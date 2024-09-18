from django import forms

from reports.models import Report

from pupils.models import Pupil


class ReportsFilterForm(forms.ModelForm):
    """Класс формы фильтрации отчётов"""
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'pupil': forms.Select(attrs={'class': 'form-select'}),
            'start_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': '2024-01-01'}),
            'end_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': '2024-01-01'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(ReportsFilterForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'
        self.fields['pupil'].required = False

        self.fields['start_period'].required = False

        self.fields['end_period'].required = False


class CreateReportForm(forms.ModelForm):
    """Класс формы создания отчётов"""
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'pupil': forms.Select(attrs={'class': 'form-select'}),
            'start_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': '2024-01-01'}),
            'end_period': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': '2024-01-01'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(CreateReportForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'


class UpdateReportForm(forms.ModelForm):
    """Класс формы обновления данных отчёта"""
    class Meta:
        model = Report
        fields = '__all__'
        widgets = {
            'pupil': forms.Select(attrs={'class': 'form-select'}),
            'start_period': forms.DateInput(attrs={'class': 'form-control start-period-updater', 'type': 'date', 'placeholder': '2024-01-01'}),
            'end_period': forms.DateInput(attrs={'class': 'form-control end-period-updater', 'type': 'date', 'placeholder': '2024-01-01'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None) 
        super(UpdateReportForm, self).__init__(*args, **kwargs)

        self.fields['pupil'].queryset = Pupil.objects.filter(owner=self.user, is_active=True)
        self.fields['pupil'].empty_label = 'Выбери ученика'
