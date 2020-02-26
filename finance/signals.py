from .models import Profile,Trasaction,Amount
from django.contrib.auth.models import Group,User
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django.dispatch import receiver




# sender = The model class.
# instance = The actual instance being saved.
# update_fields The set of fields to update as passed to Model.save(),
# or None if update_fields wasn’t passed to save().
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwarg):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        Profile.objects.create(user=instance,name=instance.username)
        print("profile created")
# post_save.connect(create_profile,sender=User)



@receiver(post_save,sender=User)
def update_profile(sender,instance,created,**kwarg):
    if created == False:
        instance.profile.save()
        print("profile updated")



# post_save.connect(update_profile,sender=User)
# @receiver(post_save,sender=Trasaction)
# def create_transaction(sender,instance,created,**kwarg):
#
#     amount = Amount.objects.get(name=instance.amount)
#
#     if created:
#          amount.balance = int(amount.balance) + int(instance.transaction_amount)
#          amount.save()
#     if created == False:
#         pass

# @receiver(pre_save,sender=Trasaction)
# def update_account(sender,instance,**kwarg):
#     amount = Amount.objects.get(name=instance.amount)
#     if not instance._state.adding:
#         amount.balance = int(amount.balance) - int(instance.transaction_amount)
#         amount.save()


# @receiver(post_save,sender=Trasaction)
# def update_transaction(sender,instance,created,**kwarg):
#     amount = Amount.objects.get(name=instance.amount)
#
#     if created == False:
#         amount.balance = int(amount.balance) + int(instance.transaction_amount)
#         amount.save()
#
@receiver(post_delete,sender=Trasaction)
def delete_transaction(sender,instance,**kwargs):
    amount = Amount.objects.get(name=instance.amount)
    amount.balance = int(amount.balance) - int(instance.transaction_amount)
    amount.save()
