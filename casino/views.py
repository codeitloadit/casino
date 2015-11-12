from django.contrib import auth, messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse


def index(request):
    return TemplateResponse(request, 'index.html')


def register(request):
    username = password = confirm = error = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')
        if not username or not password or not confirm:
            error = messages.error(request, 'All fields are required!') or True
        if password != confirm:
            error = messages.error(request, 'Passwords did not match!') or True
        if not error:
            try:
                User.objects.create_user(username=username, password=password)
            except IntegrityError:
                error = messages.error(request, 'That username is already taken!') or True
        if not error:
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
    context = {'username': username, 'password': password, 'confirm': confirm}
    return TemplateResponse(request, 'register.html', context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('index'))
        messages.error(request, 'Invalid username and/or password!')
    return TemplateResponse(request, 'login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
