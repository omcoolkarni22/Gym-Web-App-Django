# Generated by Django 3.0.5 on 2020-04-13 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gym_App', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer_register',
            name='latitude',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='trainer_register',
            name='longitude',
            field=models.CharField(max_length=80),
        ),
    ]
