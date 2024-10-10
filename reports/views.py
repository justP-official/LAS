from django.urls import reverse_lazy
from django.http import HttpResponse, Http404, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from transliterate import slugify

from reports.models import Report

from reports.forms import ReportsFilterForm, CreateReportForm, UpdateReportForm

from reports.utils import generate_pdf, convert_pdf_to_png

from user.utils import verify_owner


class ReportsListView(LoginRequiredMixin, ListView):
    """Класс представления для страницы со списком отчётов"""
    template_name = 'reports/reports_list.html'
    context_object_name = 'reports'
    paginate_by = 5

    def get_queryset(self):
        reports = Report.objects.filter(pupil__owner=self.request.user).select_related('pupil')

        pupil = self.request.GET.get('pupil', None)

        start_period = self.request.GET.get('start_period', None)

        end_period = self.request.GET.get('end_period', None)

        if pupil:
            reports = reports.filter(pupil__id=pupil)

        if start_period:
            reports = reports.filter(start_period__gte=start_period)

        if end_period:
            reports = reports.filter(end_period__lte=end_period)

        return reports

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # при создании формы передаём в неё пользователя
        context['form'] = ReportsFilterForm(data=self.request.GET, user=self.request.user) 
        context['title'] = 'L.A.S - Отчёты'
        return context


class CreateReportView(LoginRequiredMixin, CreateView):
    """Класс представления для страницы создания отчёта"""
    template_name = 'reports/create_report.html'
    form_class = CreateReportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Создать отчёт'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CreateReportView, self).get_form_kwargs()
        # при создании формы передаём в неё пользователя
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        return super().form_valid(form)


class ReadReportView(LoginRequiredMixin, DetailView):
    """Класс представления для страницы просмотра отчёта"""
    template_name = 'reports/read_report.html'
    context_object_name = 'report'
    model = Report
    pk_url_kwarg = 'report_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Просмотр отчёта'
        return context
    
    def get_object(self, report_id=None, queryset=None):
        try:
            if report_id is None:
                report_id = self.kwargs.get(self.pk_url_kwarg)

            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            report = None
        finally:
            return report
    
    def get(self, request, report_id, *args, **kwargs):
        report = self.get_object(report_id)

        if report is not None:
            if verify_owner(report.pupil.owner, self.request.user):
                return super().get(request, report_id, *args, **kwargs)
            else:
                raise PermissionDenied()
        raise Http404()


class UpdateReportView(LoginRequiredMixin, UpdateView):
    """Класс представления для страницы обновления данных отчёта"""
    template_name = 'reports/update_report.html'
    form_class = UpdateReportForm
    model = Report
    context_object_name = 'report'
    pk_url_kwarg = 'report_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Обновить данные отчёта'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(UpdateReportView, self).get_form_kwargs()
        # при создании формы передаём в неё пользователя
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_object(self, report_id=None, queryset=None):
        try:
            if report_id is None:
                report_id = self.kwargs.get(self.pk_url_kwarg)

            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            report = None
        finally:
            return report
    
    def get(self, request, report_id, *args, **kwargs):
        report = self.get_object(report_id)

        if report is not None:
            if verify_owner(report.pupil.owner, self.request.user):
                return super().get(request, report_id, *args, **kwargs)
            else:
                raise PermissionDenied()
        raise Http404()

    def post(self, request, report_id, *args, **kwargs):
        report = self.get_object(report_id)

        if report is not None:
            if verify_owner(report.pupil.owner, self.request.user):
                return super().post(request, report_id, *args, **kwargs)
            else:
                raise PermissionDenied()
        raise Http404()

class DeleteReportView(LoginRequiredMixin, DeleteView):
    """Класс представления для удаления отчёта"""
    model = Report
    success_url = reverse_lazy('reports:reports_list')
    pk_url_kwarg = 'report_id'
    
    def get_object(self, report_id=None, queryset=None):
        try:
            if report_id is None:
                report_id = self.kwargs.get(self.pk_url_kwarg)

            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            report = None
        finally:
            return report
    
    def post(self, request, report_id, *args, **kwargs):
        report = self.get_object(report_id)

        if report is not None:
            if verify_owner(report.pupil.owner, self.request.user):
                return super().post(request, report_id, *args, **kwargs)
            else:
                raise PermissionDenied()
        raise Http404()
    

class GetReportPeriod(LoginRequiredMixin, View):
    """Класс представления для получения периода отчёта"""
    def get_object(self, report_id=None, queryset=None):
        try:
            if report_id is None:
                report_id = self.kwargs.get(self.pk_url_kwarg)

            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            report = None
        finally:
            return report
    
    def get(self, request, report_id):
        report = self.get_object(report_id)

        if report is not None:
            response_data = {
                'start_period': report.start_period,
                'end_period': report.end_period
                }

            return JsonResponse(response_data)
        else:
            raise Http404()


class SaveReportAsPdf(View):
    """Класс представления для сохранения отчёта в формате pdf"""
    def get_object(self, report_id=None, queryset=None):
        try:
            if report_id is None:
                report_id = self.kwargs.get(self.pk_url_kwarg)

            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            report = None
        finally:
            return report
    
    def get(self, request, report_id):
        report = self.get_object(report_id)

        if report is not None:
            pdf_file = generate_pdf(report, request)

            filename = slugify(str(report))

            response = HttpResponse(pdf_file, content_type='application/pdf', headers={
                'Content-Disposition': f'attachment; filename="{filename}.pdf"'
            })

            return response
        else:
            raise Http404()


class SaveReportAsPng(View):
    """Класс представления для сохранения отчёта в формате png"""
    def get_object(self, report_id, queryset=None):
        return Report.objects.get(id=report_id)
    
    def get(self, request, report_id):
        report = self.get_object(report_id)

        png_file = convert_pdf_to_png(report, request)

        filename = slugify(str(report))

        response = HttpResponse(png_file, content_type='image/png', headers={
            'Content-Disposition': f'attachment; filename="{filename}.png"'
        })

        return response
