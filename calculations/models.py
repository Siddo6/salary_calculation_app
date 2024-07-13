from django.db import models

# Create your models here.

class Salary (models.Model):
    base_hours = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    extra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sunday = models.BooleanField(default=False)
    festivita = models.BooleanField(default=False)
    ferie = models.BooleanField(default=False)
    recupero = models.BooleanField(default=False)
    daily_pay=  models.DecimalField(max_digits=10, decimal_places=2)
    day = models.DateField(unique=True)
    base_start_time=  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    base_end_time=  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_start_time=  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    extra_end_time=  models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
         return f"Salary for {self.day}"
    