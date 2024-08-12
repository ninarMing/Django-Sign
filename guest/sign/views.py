from django.contrib import auth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
import time

# Create your views here.
# 账号：lai 密码：123456ming
# 账号：admin 密码：admin123456
from guest.decorators import define_login_required
from sign.models import Event, Guest


def index(request):
    return render(request, "sign/index.html")


def login_action(request):
    if request.method == 'POST':
        """可以使用‘request.POST[username]’
        但是更为安全的做法是使用request.POST.get('key',default=None,可以避免不存在时抛出异常)
        如果数据为空，则返回空字符串；
        """
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
        # if username == 'admin' and password == 'admin123':
            response = HttpResponseRedirect('event_manage')
            """
            cookie_value = username+str(time.time())
            response.set_cookie('user', cookie_value, 3600)
            """
            # request.session['user'] = username
            return response

        else:
            return render(request, 'sign/index.html', {'error': 'username or password error!'})


@define_login_required()
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get("user", '')
    #username = request.COOKIES.get('user', '')
    return render(request, 'sign/event_manage.html', {'user': username, "events": event_list})

@define_login_required()
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__icontains=search_name)
    return render(request, 'sign/event_manage.html', {'user': username, "events": event_list})

@define_login_required()
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 5)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    return render(request, 'sign/guest_manage.html', {"user": username, "guests": contacts})

@define_login_required()
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, "sign/sign_index.html", {'event': event})

@define_login_required()
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, "sign/sign_index.html", {'event': event, 'hint': 'phone error'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    if not result:
        return render(request, 'sign/sign_index.html', {'event': event, 'hint': 'event id or phone error.'})
    result = Guest.objects.filter(phone=phone, event_id=eid)
    realname = result.values('realname').first()['realname']
    phone = result.values('phone').first()['phone']
    if result.values('sign').first()['sign']:
        return render(request, 'sign/sign_index.html', {'event': event, 'hint': 'user has sign in.', 'realname': realname, 'phone': phone})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign/sign_index.html', {'event': event, 'hint': 'sign in success.', 'realname': realname,'phone': phone})


@define_login_required()
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('index.html')
    return response
