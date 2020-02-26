from django.http import HttpResponse
from django.shortcuts import redirect

def anauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return view_func(request,*args,**kwargs)
        else:
            return redirect('/login')

    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():               # Если группа существует
                group = request.user.groups.all()[0].name  # Получить имя группы
            if group in allowed_roles:                     # Если группа в списке разрешенных
                return view_func(request,*args,**kwargs)   # Вернуть вид страницы
            else:
                return HttpResponse("you are not authorized to view this page")
        return wrapper_func
    return decorator
