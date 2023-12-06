from django.contrib import admin
from .models import AppUser, Income, Budget, Expense

# Register your models here.
admin.site.register(AppUser)
admin.site.register(Income)
admin.site.register(Budget)
admin.site.register(Expense)

