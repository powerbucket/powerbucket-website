from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [   
    path('registration/', views.registration, name='registration'),
    path('submission/', views.submission, name='submission'),
    path('change_settings/', views.change_settings, name='change_settings'),
    path('readings/', views.ReadingView.as_view(), name='reading_list'),
    path('update_readings/', views.update_readings, name='update_readings'),
    path('manual_settings/', views.manual_settings, name='manual_settings'),
]

