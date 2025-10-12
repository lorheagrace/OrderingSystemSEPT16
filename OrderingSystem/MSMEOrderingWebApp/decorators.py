def login_required_session(allowed_roles=None):
    def decorator(view_func):
        @wraps(view_func)
        @never_cache
        def wrapper(request, *args, **kwargs):
            user_type = request.session.get('user_type')

            # Not logged in
            if not user_type:
                return redirect('login')

            # Logged in but not allowed
            if allowed_roles and user_type not in allowed_roles:
                # Redirect to their role-specific home page instead of another dashboard
                redirect_map = {
                    'owner': 'dashboard',  # owner's main page
                    'cashier': 'cashier_pos',  # cashier’s main POS page
                    'rider': 'deliveryrider_home',
                    'customer': 'customer_home'
                }
                return redirect(redirect_map.get(user_type, 'login'))

            # Allowed
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
