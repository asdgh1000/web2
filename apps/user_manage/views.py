from django.shortcuts import render
from .forms import LoginForm
from django.contrib import auth
from django.http import HttpResponseRedirect

# Create your views here.


def login(request):
    wrong_passed = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                wrong_passed = True
    else:
        form = LoginForm()
    return render(request, 'user_manage/login.html', {'form': form, 'password_is_wrong': wrong_passed})
