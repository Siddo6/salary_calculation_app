from django import forms
from .models import Salary

class WorkHoursForm(forms.Form):
    day = forms.DateField(required=True, label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    base_start_time = forms.IntegerField(
        label='Base Start Time', 
        required=False
    )
    base_end_time = forms.IntegerField(
        label='Base End Time', 
        required=False
    )
    extra_start_time = forms.IntegerField(
        label='Extra Start Time', 
        required=False
    )
    extra_end_time = forms.IntegerField(
        label='Extra End Time', 
        required=False
    )
    sunday = forms.BooleanField(required=False, label='Sunday')
    festivita = forms.BooleanField(required=False, label='Holiday')
    ferie = forms.BooleanField(required=False, label='Vacation')
    recupero = forms.BooleanField(required=False, label='Recovery')
    
    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        ferie = cleaned_data.get('ferie')
        recupero = cleaned_data.get('recupero')
        base_start_time = cleaned_data.get('base_start_time')
        base_end_time = cleaned_data.get('base_end_time')
        extra_start_time = cleaned_data.get('extra_start_time')
        extra_end_time = cleaned_data.get('extra_end_time')

        # Check if at least one of ferie or recupero is selected
        if not ferie and not recupero:
             # Check if at least one pair of start and end times is provided
            base_times_provided = base_start_time is not None and base_end_time is not None
            extra_times_provided = extra_start_time is not None and extra_end_time is not None
            if not (base_times_provided or extra_times_provided):
                raise forms.ValidationError("At least one of Base start/end time or Extra start/end time is required when vacation or recovery is not chosen.")

        # Check if data already exists for the given day
        if day:
            existing_salary = Salary.objects.filter(day=day).exists()
            if existing_salary:
                raise forms.ValidationError(f"Data already exists for {day}. Please choose a different day.")

        return cleaned_data
    
    
class SelectDataForm(forms.Form):
     year = forms.ChoiceField(
        choices=[(year, year) for year in range(2024, 2036)],
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 200px; text-align: center; height:1.6rem'})
    )
     month = forms.ChoiceField(
        choices=[
            ('01', 'Janar'), ('02', 'Shkurt'), ('03', 'Mars'), ('04', 'Prill'),
            ('05', 'Maj'), ('06', 'Qershor'), ('07', 'Korrik'), ('08', 'Gusht'),
            ('09', 'Shtator'), ('10', 'Tetor'), ('11', 'Nentor'), ('12', 'Dhjetor')
        ],
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'width: 200px; text-align: center;height:1.6rem'})
    )
     labels = {
            'year': 'Viti',
            'month': 'Muaji'
        }
     
     