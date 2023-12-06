from io import open_code
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class AppUser(User):
    profile_picture = models.ImageField(blank=True, null=True, upload_to="images/")

    def __str__(self):
        return self.username

class Income(models.Model):
    period = models.CharField(max_length=100000)
    amount = models.IntegerField()
    initial_income = models.IntegerField(null=True,blank=True)
    created_by = models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(blank=True, default=datetime.now)

    def __str__(self):
        return self.period
        
    #EDIT
    # @property
    # def _get_year(self):
    #     return 

class Budget(models.Model):
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    initial_budget = models.IntegerField(null=True, blank=True)
    created_by = models.ForeignKey(AppUser, null=True, blank=True, on_delete=models.CASCADE)
    income_from = models.ForeignKey(Income, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name

class Expense(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=300)
    entry_date = models.DateTimeField(default=datetime.now, blank=True)
    amount = models.IntegerField(default=00)
    transaction_type = models.CharField(null=True, max_length=40)
    budget_deducted_from = models.ForeignKey(Budget, on_delete=models.CASCADE)
    created_by = models.ForeignKey(AppUser, null=True, blank=True, on_delete=models.CASCADE)
    # transaction_number = models.CharField(max_length=20, null=False, default="TRBS0000")
    
    def __str__(self):
        return self.name