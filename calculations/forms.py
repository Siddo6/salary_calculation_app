from django import forms

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