from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from functools import wraps

def login_required_session(allowed_roles=None):
    def decorator(view_func):
        @wraps(view_func)
        @never_cache
        def wrapper(request, *args, **kwargs):
            # Allow access to login/logout without checks
            if request.resolver_match and request.resolver_match.url_name in ['login', 'logout']:
                return view_func(request, *args, **kwargs)

            user_type = request.session.get('user_type')

            # Not logged in
            if not user_type:
                return redirect('login')

            # Logged in but not allowed
            if allowed_roles and user_type not in allowed_roles:
                if user_type == 'owner':
                    return redirect('dashboard')
                elif user_type == 'cashier':
                    return redirect('cashier_dashboard')
                elif user_type == 'rider':
                    return redirect('deliveryrider_home')
                elif user_type == 'customer':
                    return redirect('customer_home')
                else:
                    return redirect('login')

            # Allowed → proceed
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
