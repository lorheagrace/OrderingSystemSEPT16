from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from functools import wraps

def login_required_session(allowed_roles=None):
    def decorator(view_func):
        @wraps(view_func)
        @never_cache
        def wrapper(request, *args, **kwargs):
            current_view = request.resolver_match.url_name if request.resolver_match else None

            # Prevent loops on login/logout
            if current_view in ['login', 'logout']:
                return view_func(request, *args, **kwargs)

            user_type = request.session.get('user_type')

            # Not logged in → go to login page
            if not user_type:
                return redirect('login')

            # Role restriction
            if allowed_roles and user_type not in allowed_roles:
                redirect_map = {
                    'owner': 'dashboard',
                    'cashier': 'cashier_dashboard',
                    'rider': 'deliveryrider_home',
                    'customer': 'customer_home'
                }
                return redirect(redirect_map.get(user_type, 'login'))

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
