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
    base_start_time=  models.IntegerField(null=True, blank=True)
    base_end_time=   models.IntegerField(null=True, blank=True)
    extra_start_time=   models.IntegerField(null=True, blank=True)
    extra_end_time=   models.IntegerField(null=True, blank=True)
    
    
    def calculate_salary(self):
        default_hourly_pay = 420
        daily_pay = 0
        base_hours = 0
        extra = 0

        if self.festivita:
            default_hourly_pay += 420 * 0.25

        if self.sunday:
            default_hourly_pay += 420 * 0.25

        if self.base_start_time is not None and self.base_end_time is not None:
            for hour in range(self.base_start_time, self.base_end_time):
                if hour > 21.00 or hour < 6.00:
                    hourly_pay = default_hourly_pay + 420 * 0.5
                elif 18.00 < hour < 22.00:
                    hourly_pay = default_hourly_pay + 420 * 0.2
                else:
                    hourly_pay = default_hourly_pay
                daily_pay += hourly_pay
                base_hours += 1

        if self.extra_start_time is not None and self.extra_end_time is not None:
            for hour in range(self.extra_start_time, self.extra_end_time):
                if hour > 21.00 or hour < 6.00:
                    hourly_pay = default_hourly_pay + 420 * 0.5 + 420 * 0.25
                elif 18.00 < hour < 22.00:
                    hourly_pay = default_hourly_pay + 420 * 0.2 + 420 * 0.25
                else:
                    hourly_pay = default_hourly_pay + 420 * 0.25
                daily_pay += hourly_pay
                extra += 1

        if self.recupero or self.ferie:
            base_hours = 6
            daily_pay = base_hours * 420 + daily_pay if extra else base_hours * 420

        self.daily_pay = daily_pay
        self.base_hours = base_hours
        self.extra = extra
        self.save()

        return daily_pay, base_hours, extra
    
    def __str__(self):
         return f"Salary for {self.day}"
    
    class Meta:
        ordering = ['day']
        
    