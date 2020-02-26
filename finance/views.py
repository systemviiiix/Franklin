# Local imports
from .models import Amount, Trasaction, Budget
from .models import Budget
from .models import Profile
from .decorators import anauthenticated_user, allowed_users
from .forms import addTransaction, NewAmount, CreateUserForm, UserLoginForm
from .filters import TrnFilter
# django imports
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Contrib imports
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.contrib import messages
from django.db.models import Count, Min, Sum, Avg


# BaseView----------------------------------------------------------------------
def base(request):
    return render(request, 'finance/base.html')


# UserAuthenticationVies

# User Registration view--------------------------------------------------------
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():

            user = form.save()

            username = form.cleaned_data.get('username')
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            #profile = Profile.objects.create(user=user,#name=user.username)
            #profile.save()
            messages.success(request, "Account was created for" + username)
            return redirect('/login')
    context = {'form': form}
    return render(request, 'finance/register.html', context)

# Login Page View---------------------------------------------------------------
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/user')
        else:
            messages.info(request, "Username or password is incorrect")
    context = {}
    return render(request, 'finance/login.html', context)


# Logout User-------------------------------------------------------------------
def logoutUser(request):
    logout(request)
    return redirect('/login')



# User Main page
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user_page(request):

    all_user_accounts = request.user.profile.amount_set.all()
    profile_transactions = request.user.profile.trasaction_set.all()
    amount_balance = float()
    # Account summ calculation for each account
    for account in all_user_accounts:
        a = profile_transactions.filter(amount=account.id).aggregate(all_cost=Sum(('transaction_amount')))
        if a['all_cost'] != None:
            account.balance = a["all_cost"]
            account.save()
            # All_amount_balance
            amount_balance = amount_balance + account.balance

    income = []
    outcome = []
    for i in profile_transactions:
        if i.transaction_amount > 0:
            income.append(i.transaction_amount)
        if i.transaction_amount < 0:
            outcome.append(i.transaction_amount)

    print(sum(income))
    print(sum(outcome))

    # all_cost = request.user.profile.trasaction_set.all().filter(amount=35).aggregate(all_cost=Sum(('transaction_amount')))
    # print(all_cost["all_cost"])
    #amount_balance = all_cost["all_cost"]
    #Сумма всех транзакций
    # Filter--------------------------------------------------------------------
    transactions = request.user.profile.trasaction_set.all()
    count = len(transactions)
    myFilter = TrnFilter(request.GET, queryset=transactions)
    transactions = myFilter.qs


    # Pagination----------------------------------------------------------------
    from django.core.paginator import Paginator
    transaction_list = transactions #transactions = Trasaction.objects.all()
    paginator = Paginator(transaction_list, 8)  # Show 4 object per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    # Delete selected items-----------------------------------------------------
    if request.POST.get('delete'):
        print(request.POST.getlist("item"))
        obj = Trasaction.objects.filter(id__in=request.POST.getlist('item'))
        obj.delete()
        #transactions.filter(id__in=request.POST.getlist('item')).delete()
        return redirect('user')


    # Data rendered to page
    context = {"page_obj": page_obj,
                "transactions":transactions,
                "myFilter": myFilter,
                'count':count,
                'amount_balance':amount_balance,
                'count_range':range(0,count-1,count),
                'income':sum(income),
                'outcome':sum(outcome)
                        }
    return render(request,'finance/user_page.html',context)



# Amounts ListView---------------------------------------------------------------
def amounts(request):
    context = {'amounts':request.user.profile.amount_set.all()}
    if (request.GET.get('DeleteButton')):
        a = request.user.profile.amount_set.all().filter(id=request.GET.get('DeleteButton'))
        #amount = Amount.objects.get(name=t[0].amount)
        a.delete()
        return redirect('/amounts')
    return render(request, 'finance/amounts.html', context)

# Dashboard view-----------------------------------------------------------------

# @allowed_users(allowed_roles=['admin'])
# def dashboard(request):
#     # Delete transaction---------------------------------------------------------
#     if (request.GET.get('DeleteButton')):
#         t = Trasaction.objects.filter(id=request.GET.get('DeleteButton'))
#         amount = Amount.objects.get(name=t[0].amount)
#         t_value = t[0].transaction_amount
#         amount.balance = amount.balance - t_value
#         amount.save()
#         Trasaction.objects.filter(id=request.GET.get('DeleteButton')).delete()
#         return redirect('/dashboard')
#     # ---------------------------------------------------------------------------
#     # amounts = Amount.objects.all()
#     # transactions = Trasaction.objects.all()
#     # for i in amounts:
#     #     for b in transactions:
#     #         if i.name == b.amount.name:
#     #             i.balance = i.balance - b.transaction_amount
#     #             i.save()
#     # Filter--------------------------------------------------------------------
#     transactions = Trasaction.objects.all()
#     count = len(transactions)
#     myFilter = TrnFilter(request.GET, queryset=transactions)
#     transactions = myFilter.qs
#
#
#     # Pagination----------------------------------------------------------------
#     from django.core.paginator import Paginator
#     transaction_list = transactions #transactions = Trasaction.objects.all()
#     paginator = Paginator(transaction_list, 4)  # Show 4 object per page.
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     # Amounts summ--------------------------------------------------------------
#     x = int()
#     for i in Amount.objects.all():
#         x = x + i.balance
#     # Context-------------------------------------------------------------------
#     context = {'amounts': Amount.objects.all(), 'transaction': transactions,
#                "myFilter": myFilter,
#                                                 "count": count,
#                                                 "balance": x,
#                                                 "page_obj": page_obj
#                }
#     # --------------------------------------------------------------------------
#     return render(request, 'finance/home.html', context)

@anauthenticated_user
def budget(request):
    budgets = Budget.objects.all()
    context = {"budgets": budgets}
    return render(request, 'finance/budget.html', context)


# Create new transaction--------------------------------------------------------
def AddNew(request):
    current_user = request.user
    form = addTransaction(request.POST)
    #form.save(commit=False)
    form.fields["amount"].queryset = request.user.profile.amount_set.all()
    if form.is_valid():
        print("valid")
        object = form.save(commit=False) # commit = False предоставляет объект модели
        object.profile = current_user.profile
        object.transaction_amount = request.POST.get('transaction_amount')
        object.save()
        # current_account = Amount.objects.get(id=request.POST.get('amount'))
        # current_account.balance = current_account.balance
        return redirect('user')
        #Function count transaction summ and add to amount balance
        #TESTING_______________________________________________________________
        # all_user_accounts = request.user.profile.amount_set.all()
        # accounts = []
        # for i in all_user_accounts:
        #     if i not in accounts:
        #         accounts.append(i)
            # for x in accounts:
            #     print(x.trasaction_set.all())
        # print("Accounts set")
        # print(accounts)
        # print("---------------------------")
        # print(f"transaction set of account {accounts[0].name}:")
        # print("----------------------------")
        # print(accounts[0].trasaction_set.all())
        # print(f'len of transaction set {len(accounts[0].trasaction_set.all())}')
        # for i in accounts:
        #     for x in i.trasaction_set.all():
        #         print(x.name)
        #         print(x.transaction_amount)
        # print("id-------------------------------")
        # print(accounts[0].id)
        # print(Trasaction.objects.filter(amount_id=17).count())
        #Author.objects.annotate(total_pages=Sum('book__pages'))
            #x = all transactions in amount i = amount
            #     i.balance += int(x.transaction_amount)
            #     i.save()
        #print(form.cleaned_data['profile'])
        # form = form.cleaned_data
        # form['profile'] = current_user.profile
        #form.fields['profile'] = current_user.profile.name
        #form.fields['transaction_amount'] = 2000
        #print(form.cleaned_data['profile'])
        #b.entry_set.add(e)
        #form.profile = current_user.profile.id
        #print(form.profile)
        #amount = Amount.objects.get(name=form.cleaned_data.get("amount"))
        # Получить значение суммы транзакции
        #t_value = form.cleaned_data.get("transaction_amount")
        # Прибавить к балансу счета сумму транзакции
        #amount.balance = amount.balance + t_value
        #amount.save()  # Сохранить счет в базе данных
        #form.save()


    context = {'form': form}
    return render(request, 'finance/new.html', context)

# DeleteTransctionView----------------------------------------------------------


def transe_delete(request):
    #transaction = get_object_or_404(Trasaction, pk=pk)  # Get your current cat
    if (request.GET.get('DeleteButton')):
        a = Trasaction.objects.filter(id=request.GET.get('DeleteButton'))
        a.delete()
        return redirect('/user')             # Finally, redirect to the homepage.


# Trasaction Update
def transaction_update(request,pk):
    f = request.user.profile.trasaction_set.all().get(id=pk)
    current_account = Amount.objects.get(id=f.amount.pk)
    form = addTransaction(request.POST,instance=f)
    form.fields["amount"].queryset = request.user.profile.amount_set.all()
    if form.is_valid():
        object = form.save(commit=False)
        amount = Amount.objects.get(name=form.cleaned_data.get("amount"))
        t_value = form.cleaned_data.get("transaction_amount")
        object.save()
        return redirect('/user')
    return render(request, 'finance/transaction_form.html', {'form': form,'values':f})


# NewAmountView-----------------------------------------------------------------
def new_amount(request):
    current_user = request.user
    form = NewAmount(request.POST)
    if form.is_valid():
        if form.is_valid():
            object = form.save(commit=False) # commit = False предоставляет объект модели
            object.profile = current_user.profile
            object.save()
        return redirect('/amounts')
    return render(request, 'finance/new_amount.html', {'form': form})


class TransactionUpdate(UpdateView):
    model = Trasaction
    fields = "__all__"
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('user')
