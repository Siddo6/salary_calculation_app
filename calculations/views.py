from django.shortcuts import render, redirect
from .forms import WorkHoursForm, SelectDataForm
from.models import Salary
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse

def calculate_salary(request):
    default_hourly_pay = 420
    daily_pay = 0
    if request.method == 'POST':
        form = WorkHoursForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            base_start_time = form.cleaned_data['base_start_time']
            base_end_time = form.cleaned_data['base_end_time']
            extra_start_time = form.cleaned_data.get('extra_start_time')
            extra_end_time = form.cleaned_data.get('extra_end_time')
            sunday = form.cleaned_data['sunday']
            festivita = form.cleaned_data['festivita']
            ferie = form.cleaned_data['ferie']
            recupero = form.cleaned_data['recupero']
            base_hours=0
            extra = 0
            if festivita:
                default_hourly_pay = default_hourly_pay + default_hourly_pay * 0.25
                
            if sunday:
                default_hourly_pay = default_hourly_pay + default_hourly_pay * 0.25
                
                
            if base_start_time is not None and base_end_time is not None:
                for hour in range(base_start_time, base_end_time):
                    if (hour > 22.00 or hour < 6.00):
                            hourly_pay = default_hourly_pay + default_hourly_pay * 0.5
                    elif (hour<22.00 and hour>19.00):
                            hourly_pay = default_hourly_pay + default_hourly_pay * 0.2
                    else:
                            hourly_pay = default_hourly_pay
                    daily_pay  = daily_pay + hourly_pay
                    base_hours+=1
            
            if extra_start_time is not None and extra_end_time is not None:            
                for hour in range(extra_start_time, extra_end_time):
                    if (hour > 22.00 or hour < 6.00):
                            hourly_pay = default_hourly_pay + default_hourly_pay * 0.5 + default_hourly_pay * 0.25
                    elif (hour<22.00 and hour>19.00):
                            hourly_pay = default_hourly_pay + default_hourly_pay * 0.2 + default_hourly_pay * 0.25
                    else:
                            hourly_pay = default_hourly_pay + default_hourly_pay * 0.25
                    daily_pay  = daily_pay + hourly_pay
                    extra+=1
                        
            if recupero or ferie:
                default_hourly_pay = default_hourly_pay
                base_hours = 6
                daily_pay = base_hours * default_hourly_pay
    
       # Create and save Salary instance
            salary_instance = Salary.objects.create(
                base_hours=base_hours,
                extra=extra,
                sunday=sunday,
                festivita=festivita,
                ferie=ferie,
                recupero=recupero,
                daily_pay=daily_pay,
                day=day,
                base_start_time=base_start_time,
                base_end_time=base_end_time,
                extra_start_time=extra_start_time,
                extra_end_time=extra_end_time
            )
            
            
        return redirect(reverse('display-salary-data'))
    else:  # Handle GET request to display the form
        form = WorkHoursForm()
    
    return render(request, 'calculations/daily-form.html', {'form': form})



def display_salary_data (request):
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year
    
    daily_datas = Salary.objects.filter(
        day__month = month,
        day__year = year
    )
    total_salary = daily_datas.aggregate(total=Sum('daily_pay'))['total'] or 0
    total_base_hours = daily_datas.aggregate(total=Sum('base_hours'))['total'] or 0    
    
    base_payment = total_base_hours * 420
    next_month_payment = total_salary - base_payment    
    context = {
        'daily_datas':daily_datas,
        'total_salary':total_salary,
        'base_payment':base_payment,
        'next_month_payment':next_month_payment
    }
    
    return render(request, 'calculations/display-salary-data.html', context)



def monthly_view (request,year, month):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get year and month from request parameters, default to current month if not provided
    year = current_year if year is None else year
    month = current_month if month is None else month
    
    daily_datas = Salary.objects.filter(
        day__month = month,
        day__year = year
    )
    total_salary = daily_datas.aggregate(total=Sum('daily_pay'))['total'] or 0
    total_base_hours = daily_datas.aggregate(total=Sum('base_hours'))['total'] or 0    
    
    base_payment = total_base_hours * 420
    next_month_payment = total_salary - base_payment
    context = {
        'daily_datas':daily_datas,
        'total_salary':total_salary,
        'base_payment':base_payment,
        'next_month_payment':next_month_payment,
        'year':year,
        'month':month
    }
    
    return render(request, 'calculations/monthly_view.html', context)



def select_datas(request):
    if request.method == 'POST':
        form = SelectDataForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']
            month = form.cleaned_data['month']
            return redirect('monthly_view', year=year, month=month)
    else:
        form = SelectDataForm()

    return render(request, 'calculations/select_datas.html', {'form': form})