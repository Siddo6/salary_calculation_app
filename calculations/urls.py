from django.urls import path
from . import views

urlpatterns = [
    path('form', views.calculate_salary, name='daily-form'),
    path('select_datas/', views.select_datas, name='select_datas'),
    path('monthly_view/<int:year>/<int:month>/', views.monthly_view, name='monthly_view'),
    path('edit/<int:pk>/', views.edit_salary, name='edit-salary'),
]