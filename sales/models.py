from django.db import models
from django.contrib.auth.models import AbstractUser




# Create your models here.
class User(AbstractUser):
    is_management = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

class Office(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="office")
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.hotel_name}"

class Activity(models.Model):
    activity = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.activity}"

class Employee(models.Model):
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    id_number = models.CharField(max_length=120)
    telephone = models.CharField(max_length=10, blank = True)
    email = models.EmailField(max_length=254, blank = True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Management(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="manager")
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)
    id_number = models.CharField(max_length=120)
    telephone = models.CharField(max_length=10, blank = True)
    email = models.EmailField(max_length=254, blank = True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

class Sale(models.Model):
    seller = models.ForeignKey(Employee, on_delete=models.SET_DEFAULT, default=1, null=True, related_name="seller")
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, related_name="hotel")
    date_sold = models.DateField(auto_now_add=True)
    activity_date = models.DateField(auto_now_add=False, blank = True)
    activity_time = models.TimeField(auto_now_add=False, blank = True)
    payment = models.CharField(max_length=254)
    room_number = models.IntegerField()
    client_name = models.CharField(max_length=254)
    client_email = models.EmailField(max_length=254, blank = True)
    quantity1 = models.IntegerField()
    activity1 = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank = True, related_name="activity1")
    price1 = models.IntegerField()
    quantity2 = models.IntegerField(blank = True, null=True)
    activity2 = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank = True, related_name="activity2")
    price2 = models.IntegerField(blank = True, null=True)
    quantity3 = models.IntegerField(blank = True, null=True)
    activity3 = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank = True, related_name="activity3")
    price3 = models.IntegerField(blank = True, null=True)
    total_cost = models.IntegerField()
    office = models.ForeignKey(Office, on_delete=models.SET_NULL, null=True, related_name="office")
    pickup_location = models.CharField(max_length=254, blank = True)
    comments = models.TextField(blank = True)


    def __str__(self):
        return f"{self.hotel}, {self.id}, {self.date_sold}"

class EmailList(models.Model):
    client_name = models.CharField(max_length=254)
    client_email = models.EmailField(max_length=254, blank = True)





