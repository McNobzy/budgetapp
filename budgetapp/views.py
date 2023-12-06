from django.shortcuts import render, redirect
from .models import Income, Budget, AppUser, Expense
from django.contrib import messages
from django.contrib.auth.models import User, auth
from datetime import datetime

# Create your views here.

def indet(request):
    try:
        if (request.user).appuser:
            if request.user.is_authenticated:
                return render(request, 'success.html')
            else:
                return redirect('login')
        else:
            return render(request, 'buffer.html')
    except:
        return render(request, 'buffer.html')
    

def index(request):
    #user = request.user
    try:
        if request.user.is_authenticated:
            if isinstance(request.user.appuser, AppUser) == True:
                pk = request.user.id
                incomes = Income.objects.filter(created_by=pk)

                inc_id = int(request.POST['income-select'])
                inc = Income.objects.get(id=inc_id)

                slicer = slice(5)
                needed_budgets = list(Budget.objects.filter(created_by=request.user.id))
                budgets = needed_budgets[slicer]
                all_expenses = list(Expense.objects.filter(created_by=request.user.id))
                expenses = all_expenses[slicer]
                # if (request.method == 'GET'):
                #     inc_id = request.GET['income-select']
                #     inc = Income.objects.get(id=inc_id)
                    
                
            else:
                messages.info(request, 'This user is not registered on this app. Sign in as a registered user')
        else:
            return redirect('login')
    except:
        return redirect('login')
        
    return render(request, 'dashboard.html', {'incomes':incomes,'budgets':budgets, 'expenses':expenses})
        # return redirect('login')

    
        # messages.info(request, "This user is not authorised to use this app")
        # return redirect('login')

    # app_user = AppUser.objects.get(id=2)
    # else:
        # return render(request, 'dashboard.html', {'incomes':incomes,'budgets':budgets, 'expenses':expenses})


def renderSortedIndex(request):
    incomes = Income.objects.filter(created_by=request.user.id)
    if request.method == 'POST':
        inc_id = int(request.POST['income-select'])
        inc = Income.objects.get(id=inc_id)

        slicer = slice(6)
        needed_budgets = list(Budget.objects.filter(created_by=request.user.id, income_from=inc))
        budgets = needed_budgets[slicer]
        all_expenses = list(Expense.objects.filter(created_by=request.user.id,budget_deducted_from__income_from=inc))
        expenses = all_expenses[slicer]

    return render(request, 'dashboard.html', {'incomes':incomes, 'budgets':budgets, 'expenses':expenses})



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Invalid credentials!')
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']        
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already exsists')
                return redirect('register')
            else:
                app_user = AppUser.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,  password=password)
                app_user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password does not match')
            return redirect('register')

    else:
        return render(request, 'register.html')


def addExpense(request):
    if request.user.is_authenticated:
        budgets = Budget.objects.filter(created_by=request.user.id)

        if request.method == "POST":
            name = request.POST['name']
            amount = int(request.POST['amount'])
            transaction_type = request.POST['transaction_type']
            budget_id = request.POST['budget']

            budget = Budget.objects.get(id=budget_id)

            new_expense = Expense.objects.create(name=name, amount=amount, transaction_type=transaction_type, budget_deducted_from=budget, created_by=request.user.appuser)
            new_expense.save()
            budget.amount = budget.amount - amount
            budget.save()
            return redirect('/')
        else:  
            return render(request, 'add-expense.html', {'budgets':budgets})
    else:
        messages.info(request, 'You cannot add expense without logging in. Please log in')
        return redirect('login')

def addBudgetCategory(request):
    incomes = Income.objects.all()
    if request.method == 'POST':
        name = request.POST['budget-name']
        amount = int(request.POST['budget-amount'])
        initial_budget = amount
        income_from = int(request.POST['income_from'])
        income = Income.objects.get(id=income_from)

        if Budget.objects.filter(name=name).exists():
            messages.info(request, "It seems that Budget named" + name + " already exists")
            return redirect('/add-budget')
        else: 
            new_budget = Budget.objects.create(name=name, amount=amount, initial_budget=initial_budget, income_from=income, created_by=request.user.appuser)
            new_budget.save()
            income.amount = income.amount - new_budget.amount
            income.save()
            return redirect('/')
    else:
        return render(request, 'add-budget-category.html', {'incomes':incomes})

def addIncome(request):
    if request.method == "POST":
        period = request.POST['period']
        amount = int(request.POST['amount'])

        new_income = Income.objects.create(period=period, amount=amount, created_by=request.user.appuser)
        initial_income = new_income.amount
        if Income.objects.filter(period=new_income.period).exists():
            new_income.delete()
            messages.info(request, "The period for this income " +str(new_income)+ " already exists. Try editing that if you want to change it")
            return redirect('/add-income')
        else:
            new_income.save()
            return redirect('/')
    else:
        return render(request, 'add-income.html')

def budgets(request):
    pass

def expenses(request):
    pass

def viewBudgetDetails(request, pk):
    budget = Budget.objects.get(id=pk)
    return render(request, 'view-budget-category.html', {'budget':budget})

def viewExpense(request, pk):
    expense = Expense.objects.get(id=pk)

    return render(request, 'view-expense.html', {'expense':expense})

def deleteBudget(request, pk):
    budget_to_delete = Budget.objects.get(id=pk)
    budget_to_delete.income_from.amount = budget_to_delete.income_from.amount + budget_to_delete.amount
    budget_to_delete.income_from.save()
    budget_to_delete.delete()

    return redirect('/')

def updateBudget(request, pk):
    incomes = Income.objects.all()
    budget = Budget.objects.get(id=pk)
    old_budget_amount = budget.amount
    if request.method == 'POST':
        name = request.POST['budget-name']
        amount = int(request.POST['amount'])
        income_from = int(request.POST['income_from'])
        income = Income.objects.get(id=income_from)

        budget.name = name
        budget.amount = amount
        budget.income_from = income
        budget.created_by = request.user.appuser
        diff = amount - old_budget_amount
        income.amount = income.amount - diff
        income.save()
        budget.save()
        return redirect('/')
    else:
       return render(request, 'edit-budget.html', {'incomes':incomes, 'budget':budget})


def deleteExpense(request, pk):
    expense_to_delete = Expense.objects.get(id=pk)
    expense_to_delete.budget_deducted_from.amount = expense_to_delete.budget_deducted_from.amount + expense_to_delete.amount
    expense_to_delete.budget_deducted_from.save()
    expense_to_delete.delete()

    return redirect('/')

def updateExpense(request, pk):
    expense = Expense.objects.get(id=pk)
    budgets = Budget.objects.filter(created_by=request.user.id)
    # incomes = Income.objects.all()
    # budget = Budget.objects.get(id=pk)
    old_expense_amount = expense.amount
    old_budget_amount = expense.budget_deducted_from.amount
    if request.method == 'POST':
        name = request.POST['expense-name']
        amount = int(request.POST['expense-amount'])
        budget_from = int(request.POST['budget-from'])
        budget = Budget.objects.get(id=budget_from)
        transactiontType = request.POST['transaction-type']

        expense.name = name
        expense.amount = amount
        expense.budget_deducted_from = budget
        difference = expense.amount - old_expense_amount
        budget.amount = budget.amount - difference
        entry_date = datetime.now
        transaction_type = transactiontType
        budget.save()
        expense.save()
        return redirect('/')
        # budget.created_by = request.user.appuser
        # diff = amount - old_budget_amount
        # income.amount = income.amount - diff
        # income.save()
        # budget.save()
        # return redirect('/')
    else:
        return render(request, 'edit-expense.html', {'expense':expense, 'budgets':budgets})


def updateIncome(request, pk):
    income = Income.objects.get(id=pk)
    if request.method == 'POST':
        period = request.POST['period']
        amount = int(request.POST['amount'])

        income.period = period
        income.amount = amount
        income.save()
        return redirect('/')

    else:
        return render(request, 'edit-income.html', {'income':income})

def addToIncome(request, pk):
    income = Income.objects.get(id=pk)
    if request.method == 'POST':
        amount = float(request.POST['amount'])

        income.amount = income.amount + amount
        income.save()
        return redirect('/')
    else:
        return render(request, 'add-to-income.html', {'income':income})

def deleteIncome(request, pk):
    pass
    # income = Income.objects.get(id=pk)
    # budgets = Budget.objects.filter(income_from=income)
    # expenses = Expense.objects.filter(budget_deducted_from = budgets)
    # income.delete()
    # return redirect('/')


def viewExpenses(request):
    expenses = Expense.objects.filter(created_by = request.user.appuser)
    budgetsOnExpensespage = Budget.objects.filter(created_by = request.user.appuser);
    incomesOnExpensespage = Income.objects.filter(created_by = request.user.appuser);


    expensesless2000 = Expense.objects.filter(amount__lte = 2000)
    expensesless4500 = Expense.objects.filter(amount__gt = 2000, amount__lte = 4500)
    expensesmore4500 = Expense.objects.filter(amount__gt = 4500)
    total_spend = 0
    for expense in expenses:
        total_spend = total_spend + expense.amount
    
    
    
    
    return render(request, 'all-expenses.html', {'incomesOnExpensesPage':incomesOnExpensespage, 'expenses':expenses, 'expensesless2000':expensesless2000, 'expensesless4500':expensesless4500, 'expensesmore4500':expensesmore4500, 'total_spend': total_spend})

def renderSortedExpenses(request):
    incomes = Income.objects.filter(created_by=request.user.id)
    if request.method == 'POST':
        inc_id = int(request.POST['income-select'])
        inc = Income.objects.get(id=inc_id)

        # slicer = slice(6)
        expenses = list(Expense.objects.filter(created_by=request.user.id, budget_deducted_from__income_from=inc))
        # expenses = needed_expenses[slicer]
        # all_expenses = list(Expense.objects.filter(created_by=request.user.id,budget_deducted_from__income_from=inc))
        # expenses = all_expenses[slicer]

        expensesless2000 = Expense.objects.filter(amount__lte = 2000, budget_deducted_from__income_from=inc)
        expensesless4500 = Expense.objects.filter(amount__gt = 2000, amount__lte = 4500, budget_deducted_from__income_from=inc)
        expensesmore4500 = Expense.objects.filter(amount__gt = 4500, budget_deducted_from__income_from=inc)
        total_spend = 0
        for expense in expenses:
            total_spend = total_spend + expense.amount

    return render(request, 'sort-expenses.html', {'incomes':incomes, 'expenses':expenses, 'expensesless2000':expensesless2000, 'expensesless4500':expensesless4500, 'expensesmore4500':expensesmore4500, 'total_spend': total_spend})