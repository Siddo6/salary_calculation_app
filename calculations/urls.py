from django.urls import path
from . import views

urlpatterns = [
    path('form', views.calculate_salary, name='daily-form'),
    path('display-salary-data/', views.display_salary_data, name='display-salary-data'),
    path('select_datas/', views.select_datas, name='select_datas'),
    path('monthly_view/<int:year>/<int:month>/', views.monthly_view, name='monthly_view'),
]