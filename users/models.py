# from django.contrib.auth.models import Group, Permission
# from django.db import models
# from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
import datetime
from courses.models import Course, Module

class UserProgress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    completed_modules = models.ManyToManyField(Module)


# Create your models here.
class MyModel(models.Model):
    fname = models.CharField(max_length=30, default='')
    lname = models.CharField(max_length=30, default='')
    email = models.EmailField()
    date = models.DateField(default=datetime.date.today)
