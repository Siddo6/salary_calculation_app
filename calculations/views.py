from django.shortcuts import render, redirect, get_object_or_404
from .forms import WorkHoursForm, SelectDataForm
from.models import Salary
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse
from django.db import IntegrityError


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
                default_hourly_pay = default_hourly_pay + 420 * 0.25
                
            if sunday:
                default_hourly_pay = default_hourly_pay + 420 * 0.25
                
                
            if base_start_time is not None and base_end_time is not None:
                for hour in range(base_start_time, base_end_time):
                    if (hour > 21.00 or hour < 6.00):
                            hourly_pay = default_hourly_pay + 420 * 0.5
                    elif (hour<22.00 and hour>18.00):
                            hourly_pay = default_hourly_pay + 420 * 0.2
                    else:
                            hourly_pay = default_hourly_pay
                    daily_pay  = daily_pay + hourly_pay
                    base_hours+=1
            
            if extra_start_time is not None and extra_end_time is not None:            
                for hour in range(extra_start_time, extra_end_time):
                    if (hour > 21.00 or hour < 6.00):
                            hourly_pay = default_hourly_pay + 420 * 0.5 + 420 * 0.25
                    elif (hour<22.00 and hour>18.00):
                            hourly_pay = default_hourly_pay + 420 * 0.2 + 420 * 0.25
                    else:
                            hourly_pay = default_hourly_pay + 420 * 0.25
                    daily_pay  = daily_pay + hourly_pay
                    extra+=1
            
            if daily_pay is not None :
                extra_pay = daily_pay
            else:
                extra_pay = None
                print(f"Extra Hour: {hour}, Hourly Pay: {hourly_pay}, Daily Pay: {daily_pay}")
                        
            if recupero or ferie:
                base_hours = 6
                if extra_pay is not None:
                    daily_pay = base_hours * 420 + extra_pay
                else:
                    daily_pay = base_hours * 420
    
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
            
            default_hourly_pay = 420
            return redirect(reverse('index'))
            
        else:
            print(form.errors)
                
    else:  # Handle GET request to display the form
        form = WorkHoursForm()
    
    return render(request, 'calculations/daily-form.html', {'form': form})


def monthly_view (request,year, month):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    # Get year and month from request parameters, default to current month if not provided
    year = current_year if year is None else year
    month = current_month if month is None else month
    
    # Calculate previous month
    prev_month = month - 1 if month > 1 else 12
    prev_year = year if month > 1 else year - 1
    
    # Calculate next month
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1
    
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
        'current_year':current_year,
        'current_month':current_month,
        'year':year,
        'month':month,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
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


def edit_salary(request, pk):
    if pk:
        salary_instance = get_object_or_404(Salary, pk=pk)
    else:
        salary_instance = None

    if request.method == 'POST':
        form = WorkHoursForm(request.POST, instance=salary_instance)
        if form.is_valid():
            try:
                
                form.save()
                salary_instance.calculate_salary()
                return redirect('index')  # Adjust redirection as necessary
            except IntegrityError as e:
                if 'unique constraint' in str(e).lower():
                    form.add_error('day', 'A salary record for this day already exists.')
                else:
                    form.add_error(None, 'An unexpected error occurred.')
        else:
            print("Form is not valid.")
            print(form.errors)
    else:
        form = WorkHoursForm(instance=salary_instance)

    return render(request, 'calculations/edit-salary.html', {'form': form, 'salary_instance': salary_instance})