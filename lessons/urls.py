from django.urls import path

from lessons import views

app_name = 'lessons'

urlpatterns = [
    path('', views.LessonsListView.as_view(), name='lessons_list'),
    path('create-lesson/', views.CreateLessonView.as_view(), name='create_lesson'),
    path('update-lesson/<int:pk>/', views.UpdateLessonView.as_view(), name='update_lesson'),
    path('delete-lesson/<int:pk>/', views.DeleteLessonView.as_view(), name='delete_lesson'),
    path('get-lesson-datetime/<int:lesson_id>/', views.GetLessonDatetime.as_view(), name='get_lesson_datetime')
]
