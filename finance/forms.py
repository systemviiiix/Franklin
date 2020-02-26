from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trasaction,Budget,Amount,Category


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserLoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']

class addTransaction(ModelForm):
    class Meta:
        model = Trasaction
        fields = ['name','category','amount','transaction_amount']#['profile','name','date','amount','transaction_amount']
        #exclude = ('profile',)

class AddBudgetColected(ModelForm):
    model = Budget
    fields = ["colected"]

class NewAmount(ModelForm):
    class Meta:
        model = Amount
        fields = '__all__'
