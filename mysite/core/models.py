from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

GENDER_CHOICES=[('Male','Male'),('Female','Female'), ('other','other')]


class Languages(models.Model):
	user = models.OneToOneField(User)
	language = models.CharField(max_length=50)
	language_type = models.CharField(max_length=6)

class Profile(models.Model):
    user = models.OneToOneField(User)
    bio = models.CharField(max_length=100)
    mode = models.CharField(max_length=6)
    country = models.CharField(max_length=15, default='India')
    city = models.CharField(max_length=50, default='Pune')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
