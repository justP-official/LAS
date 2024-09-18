from django.urls import path

from pupils import views

app_name = 'pupils'

urlpatterns = [
    path('', views.PupilsListView.as_view(), name='pupils_list'),
    path('create-pupil/', views.CreatePupilView.as_view(), name='create_pupil'),
    path('update-pupil/<int:pk>/', views.UpdatePupilView.as_view(), name='update_pupil'),
    path('get-pupil-price/<int:pupil_id>/', views.GetPupilPrice.as_view(), name='get_pupil_price')
]
