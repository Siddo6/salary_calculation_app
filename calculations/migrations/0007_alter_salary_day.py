# Generated by Django 5.0.7 on 2024-07-14 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculations', '0006_alter_salary_base_end_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='day',
            field=models.DateField(),
        ),
    ]
