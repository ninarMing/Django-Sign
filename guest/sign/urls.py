"""
URL configuration for guest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/zh-hans/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    注意：
    在Django 2.0及以后的版本中，URL的配置方式已经从正则表达式切换到基于路径的方式。
    如果你仍然在使用正则表达式，可能需要做一些调整。,re_path支持正则表达式；
    re_path(r'^$|^index+', views.index, name="index"),
"""

from django.urls import path, re_path

from . import views, views_if

urlpatterns = [
    # path支持基于路径方式；
    # path('', views.index, name='index'),
    # 正则表达式有些问题，需要优化
    re_path(r'^$|^index\.?html?$', views.index, name="index"),
    path('login_action', views.login_action, name='login_action'),
    path('event_manage', views.event_manage, name='event_manage'),
    path('search_name', views.search_name, name='search_name'),
    path('guest_manage', views.guest_manage, name='guest_manage'),
    re_path('sign_index/(?P<eid>[0-9]+)/$', views.sign_index, name='sign_index'),
    re_path('.*sign_index_action/(?P<eid>[0-9]+)/$', views.sign_index_action, name='sign_index_action'),
    path('logout', views.logout, name='logout'),

    # 不同应用可以自定义不同的登录界面
    re_path(r'.*login.*', views.index, name="login"),


    # sign接口开发
    path('api/add_event', views_if.add_event, name='add_event'),
    path('api/add_guest', views_if.add_guest, name='add_guest'),
    path('api/get_event_list', views_if.get_event_list, name='get_event_list'),
    path('api/get_guest_list',views_if.get_guest_list,name='get_guest_list'),
    # path('api/user_sign',views_if.user_sign,name='user_sign'),


]