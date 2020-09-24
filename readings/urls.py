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
    path('settings/', views.SettingsView.as_view(), name='settings_list'),
]
