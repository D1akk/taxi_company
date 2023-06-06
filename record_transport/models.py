from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    is_staff = models.BooleanField(default=False, verbose_name='Администратор')
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    

class Driver(User):
    range = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=3)
    license_number = models.CharField(max_length=40)
    license_expiry = models.DateField()
    

    def __str__(self):
        return self.first_name+' '+self.middle_name+' '+self.last_name    


class Car(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    mark = models.CharField(max_length=40)
    model = models.CharField(max_length=40)
    year = models.DateField()
    color = models.CharField(max_length=40)
    number = models.CharField(max_length=40, primary_key=True)
    mileage = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=40)
    transmission = models.CharField(max_length=40)
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1)
    pokazatel = models.FloatField(null=True)
    passangers = models.IntegerField(null=True)
    description = models.TextField()


class Task(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True,blank=True)
    title = models.CharField(max_length=200)
    client = models.CharField(max_length=100)
    price = models.CharField(max_length=20)
    people = models.IntegerField(null=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True) 
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    distance = models.FloatField(null=True, blank=True)
    fuel_before = models.FloatField(null=True, blank=True)
    fuel_after = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.title 