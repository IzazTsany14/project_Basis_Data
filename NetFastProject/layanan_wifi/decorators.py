from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    """
    Decorator for views that checks that the user is logged in and has a role
    in the allowed_roles list.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Check if user_role is in session
            if 'user_role' not in request.session:
                return redirect('login_page')

            user_role = request.session.get('user_role')
            if user_role in allowed_roles:
                # Role is allowed, proceed with the view
                return view_func(request, *args, **kwargs)
            else:
                # Role is not allowed, redirect to login page
                # Optionally, you could redirect to an 'access_denied' page
                return redirect('login_page')
        return _wrapped_view
    return decorator
