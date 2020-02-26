from django.db import models
from django.contrib.auth.models import User
import datetime



# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.name)




class Amount(models.Model):
    profile =models.ForeignKey("Profile",null=True,blank=True,on_delete=models.CASCADE)
    AMOUNT_TYPE_CHOICES = (
            ('cash', 'Cash'),
            ('card ','Card'),
        )
    name = models.CharField(max_length=120,)
    type = models.CharField(max_length=120,choices=AMOUNT_TYPE_CHOICES,default="cash")
    balance = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Trasaction(models.Model):
    profile =models.ForeignKey("Profile",null=True,blank=True,on_delete=models.CASCADE)
    category =models.ForeignKey("Category",null=True,blank=True,on_delete=models.CASCADE)
    #profile = models.OneToOneField(Profile,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    date = models.DateField(auto_now_add=True, blank=True)
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE)
    transaction_amount = models.IntegerField(max_length=9,blank=True,null=True)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)

class Category(models.Model):
    profile =models.ForeignKey("Profile",null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)

    def __str__(self):              # __unicode__ on Python 2
        return str(self.name)


class Budget(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField()
    goal = models.DecimalField(max_digits=19, decimal_places=2)
    colected = models.DecimalField(max_digits=19, decimal_places=2)
    amount = models.ForeignKey(Amount, on_delete=models.CASCADE)

    def get_procents(self):
        one = self.goal / 100
        procent_collected = self.colected / one
        return procent_collected
