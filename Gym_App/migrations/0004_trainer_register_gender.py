# Generated by Django 3.0.5 on 2020-04-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gym_App', '0003_auto_20200413_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer_register',
            name='gender',
            field=models.CharField(default='some_value', max_length=30),
        ),
    ]
