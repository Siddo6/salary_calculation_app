from django.shortcuts import render
from datetime import datetime
# Create your views here.


def index(request):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    context = {
        'current_year': current_year,
        'current_month': current_month,
    }
    return render(request, 'core/index.html', context)