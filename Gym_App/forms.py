from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Trainer_Register
        fields = ["slug", "name", "email", "age", "speciality", "qualification", "Address_of", "postcode", "telephone",
                  "aval_days",
                  "aval_time",
                  "ser_offered",
                  "profile_picture",
                  "personal_profile",
                  "additional_pic"
                  ]

