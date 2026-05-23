
from django.shortcuts import redirect
from functools import wraps

def owner_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.role == "OWNER":
            return view_func(request, *args, **kwargs)
        return redirect("home") 
    return wrapper