from django.contrib import admin
from django.urls import path
from . import views
from .views import AddNew,base,transaction_update,registerPage,loginPage,logoutUser,TransactionUpdate

urlpatterns = [
    path('',views.base,name='base'),
    path('amounts',views.amounts,name='amounts'),
    path('amounts/new_amount',views.new_amount,name='new_amount'),
    path('budget',views.budget,name='budget'),
    #path('dashboard', views.dashboard, name='dashboard'),
    path('addTransaction',views.AddNew, name = 'AddNew'),
    path('update',views.transaction_update,name='transaction_update'),
    path('transe_delete',views.transe_delete, name = 'transe_delete'),
    path("register",views.registerPage,name = 'register'),
    path('login',views.loginPage,name ='login'),
    path('logout',views.logoutUser,name ='logout'),
    path('user',views.user_page,name='user'),
    path('edit/<int:pk>', views.transaction_update, name='Transaction_edit'),

]
