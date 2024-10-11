from django.urls import path

from reports import views

app_name = 'reports'

urlpatterns = [
    path('', views.ReportsListView.as_view(), name='reports_list'),
    path('create-report/', views.CreateReportView.as_view(), name='create_report'),
    path('read-report/<int:report_id>/', views.ReadReportView.as_view(), name='read_report'),
    path('update-report/<int:report_id>/', views.UpdateReportView.as_view(), name='update_report'),
    path('delete-report/<int:report_id>/', views.DeleteReportView.as_view(), name='delete_report'),
    path('get-report-period/<int:report_id>/', views.GetReportPeriod.as_view(), name='get_report_period'),
    path('save-report-as-pdf/<int:report_id>/', views.SaveReportAsPdf.as_view(), name='save_report_as_pdf'),
    path('save-report-as-png/<int:report_id>/', views.SaveReportAsPng.as_view(), name='save_report_as_png'),
]
