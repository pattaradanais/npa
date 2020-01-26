import functools
from typing import Callable
from flask import session, flash, redirect, url_for, request, current_app


def requires_login(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('email'):
            flash('You need to be signed in for this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function

#admin@admin.com
#adminnpacs41
def requires_admin(f: Callable) -> Callable:
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('email') != current_app.config.get('ADMIN', ''):
            flash('You need to be an administrator to access this page.', 'danger')
            return redirect(url_for('users.login_user'))
        return f(*args, **kwargs)

    return decorated_function

# def scrap_success(f: Callable) -> Callable:
#     @functools.wraps(f)
#     def decorated_function(*args, **kwargs):
#         if f ==  True:
#             flash('Update Success.', 'success')
#             return redirect(url_for('admin.update_property'))
#         return f(*args, **kwargs)

#     return decorated_function