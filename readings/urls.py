from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += [   
    path('registration/', views.registration, name='registration'),
    path('submission/', views.submission, name='submission'),
    path('readings/', views.ReadingView.as_view(), name='reading_list'),
]
