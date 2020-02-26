from django.contrib import admin
from .models import Amount,Trasaction,Budget,Profile,Category
# Register your models here.

admin.site.register(Amount)
admin.site.register(Trasaction)
admin.site.register(Budget)
admin.site.register(Profile)
admin.site.register(Category)
