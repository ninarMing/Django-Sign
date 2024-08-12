from functools import wraps
from django.conf import settings
from django.contrib.auth.views import redirect_to_login

# 不同应用可以自定义不同的登录界面
def define_login_required(login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            else:
                return redirect_to_login(request.get_full_path(), login_url or settings.LOGIN_URL)
        return _wrapped_view

    """ 如果装饰器直接被使用，而不是调用的结果
    # if callable(login_url):
    #     return decorator(login_url)"""

    return decorator