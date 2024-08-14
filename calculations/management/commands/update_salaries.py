from django.core.management.base import BaseCommand
from calculations.models import Salary

class Command(BaseCommand):
    help = 'Update existing salary instances with the new calculation logic'
    def handle(self, *args, **kwargs):
        default_hourly_pay = 420
        

        for salary_instance in Salary.objects.all():
            daily_pay = 0
            base_hours = 0
            extra = 0

            if salary_instance.festivita:
                default_hourly_pay = default_hourly_pay + 420 * 0.25

            if salary_instance.sunday:
                default_hourly_pay = default_hourly_pay + 420 * 0.25
                
            print(f"Calculating for {salary_instance.day}: Festivita: {salary_instance.festivita}, Sunday: {salary_instance.sunday}")
            print(f"Initial default_hourly_pay: {default_hourly_pay}")
            
            if salary_instance.base_start_time is not None and salary_instance.base_end_time is not None:
                for hour in range(salary_instance.base_start_time, salary_instance.base_end_time):
                    if (hour > 21.00 or hour < 6.00):
                        hourly_pay = default_hourly_pay + 420 * 0.5
                    elif (hour < 22.00 and hour > 18.00):
                        hourly_pay = default_hourly_pay + 420 * 0.2
                    else:
                        hourly_pay = default_hourly_pay
                    daily_pay = daily_pay + hourly_pay
                    base_hours += 1
                    print(f"Hour: {hour}, Hourly Pay: {hourly_pay}, Daily Pay: {daily_pay}")
            if salary_instance.extra_start_time is not None and salary_instance.extra_end_time is not None:
                for hour in range(salary_instance.extra_start_time, salary_instance.extra_end_time):
                    if (hour > 21.00 or hour < 6.00):
                        hourly_pay = default_hourly_pay + 420 * 0.5 + 420 * 0.25
                    elif (hour < 22.00 and hour > 18.00):
                        hourly_pay = default_hourly_pay + 420 * 0.2 + 420 * 0.25
                    else:
                        hourly_pay = default_hourly_pay + 420 * 0.25
                    daily_pay = daily_pay + hourly_pay
                    extra += 1
            
            if daily_pay is not None :
                extra_pay = daily_pay
            else:
                extra_pay = 0
                print(f"Extra Hour: {hour}, Hourly Pay: {hourly_pay}, Daily Pay: {daily_pay}")
                    
            if salary_instance.recupero or salary_instance.ferie:
                base_hours = 6
                if extra_pay is not None:
                    daily_pay = base_hours * 420 + extra_pay
                    extra_pay = 0
                else:
                    daily_pay = base_hours * 420

            # Update the instance with the new calculations
            salary_instance.daily_pay = daily_pay
            salary_instance.base_hours = base_hours
            salary_instance.extra = extra
            salary_instance.save()
            default_hourly_pay = 420
        
            print(f"Final Daily Pay for {salary_instance.day}: {daily_pay}")
        self.stdout.write(self.style.SUCCESS('Successfully updated salary instances'))
