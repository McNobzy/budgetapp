from django.urls import path
from . import views
#jd37doe
urlpatterns = [
    path('', views.index, name='dashboard'), #done
    path('sort-by-income', views.renderSortedIndex, name='sort-income'),
    path('sort-expenses', views.renderSortedExpenses, name='sort-expenses'),
    path('add_post', views.addExpense, name='addExpense'),
    path('login', views.login, name='login'), #done
    path('register', views.register, name='register'), #done
    path('add-expense', views.addExpense, name='addExpense'), #done
    path('add-budget', views.addBudgetCategory, name="addBudgetCategory"), #done
    path('view-budget/<str:pk>', views.viewBudgetDetails, name="viewBudgetDetails"),
    path('add-income', views.addIncome, name='addIncome'), #done
    path('edit-income/<str:pk>', views.updateIncome, name='updateIncome'),
    path('addto-income/<str:pk>', views.addToIncome, name='addToIncome'),
    path('delete-income/<str:pk>', views.deleteIncome, name='deleteIncome'),
    path('budgets', views.budgets, name='budgets'),
    path('delete-budget/<str:pk>', views.deleteBudget, name='deleteBudget'),
    path('delete-expense/<str:pk>', views.deleteExpense, name='deleteExpense'), #done
    path('edit-expense/<str:pk>', views.updateExpense, name='updateExpense'),
    path('edit-budget/<str:pk>', views.updateBudget, name='updateBudget'), 
    path('expenses', views.viewExpenses, name='viewExpenses'), 
    path('expense/<str:pk>', views.viewExpense, name='viewEpxense'), #done
    path('logout', views.logout, name='logout') #done
]