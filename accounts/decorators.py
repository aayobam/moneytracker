from django.shortcuts import redirect



"""
Ensures that no authenticated user has access to registeration and login url or page
import this modul on the views and place the @unauthenticated_user decorator above the registeration
and login function views.
"""
def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("budget_list")
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function
