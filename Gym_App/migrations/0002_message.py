# Generated by Django 3.0.5 on 2020-04-13 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gym_App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_of_tra', models.CharField(max_length=100)),
                ('name_of_cli', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]
