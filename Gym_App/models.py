from django.db import models
import pgeocode
from django.utils.text import slugify
# Create your models here.


class Trainer_Register(models.Model):
    slug = models.SlugField(unique=True, null=True)
    name = models.CharField(max_length=100, default="some_value")
    email = models.CharField(max_length=30, default="some_value")
    age = models.IntegerField()
    gender = models.CharField(max_length=30, default="some_value")
    speciality = models.CharField(max_length=100)
    qualification = models.CharField(max_length=30)
    Address_of = models.CharField(max_length=80)
    postcode = models.IntegerField()
    longitude = models.CharField(max_length=80)
    latitude = models.CharField(max_length=80)
    telephone = models.CharField(max_length=30)
    aval_days = models.IntegerField()
    aval_time = models.IntegerField()
    ser_offered = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile', null=True, verbose_name="")
    personal_profile = models.CharField(max_length=500)
    additional_pic = models.ImageField(upload_to='additional', null=True, verbose_name="")

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        if self.postcode:
            nomi = pgeocode.Nominatim('us')
            details = nomi.query_postal_code(str(self.postcode))
            self.longitude = details['longitude']
            self.latitude = details['latitude']
        """if self.latitude == 'Nan' or self.longitude == 'NaN':
            self.latitude = 0
            self.longitude = 0"""
        super(Trainer_Register, self).save(*args, **kwargs)


class Client_Register(models.Model):
    email = models.CharField(max_length=30, default="some_value")
    name = models.CharField(max_length=30, default="some_value")
    age = models.IntegerField()
    Address = models.CharField(max_length=80)
    postcode = models.IntegerField()
    telephone = models.IntegerField()
    aval_days = models.IntegerField()
    aval_time = models.IntegerField()
    longitude = models.IntegerField(default="1")
    latitude = models.IntegerField(default="1")

    def save(self, *args, **kwargs):
        if self.postcode:
            nomi = pgeocode.Nominatim('us')
            details = nomi.query_postal_code(str(self.postcode))
            self.longitude = details['longitude']
            self.latitude = details['latitude']

        super(Client_Register, self).save(*args, **kwargs)


class Message(models.Model):
    name_of_tra = models.CharField(max_length=100)
    name_of_cli = models.CharField(max_length=100)
    message = models.TextField()
