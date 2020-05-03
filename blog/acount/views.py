from django.shortcuts import render
from django.http import HttpResponse
from acount.form import LoginForm, RegistrationForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)  # 可以不是用表单，直接操作参数
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponse("Welcom, you have been authenticated successfully!")
            else:
                return HttpResponse("Sorry, you name or password was wrong!")
        else:
            return HttpResponse("Invalid login!")
    elif request.method == 'GET':
        login_form = LoginForm()
        # user = request.user
        # if user.is_authenticated:
        #     return HttpResponse('您已登陆，请继续其他操作')
        return render(request, 'acount/login.html', {'form': login_form})


def logout_def(request):
    logout(request)
    return render(request, 'acount/logout.html')


def register(request):
    if request.method == 'POST':
        register_form = RegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save(commit=False)
            new_user.set_password(register_form.cleaned_data['password'])
            profile_user = profile_form.save(commit=False)
            profile_user.user = new_user
            new_user.save()
            profile_form.save()
            return HttpResponse("successfully")
        else:
            return HttpResponse("sorry, your can not register")
    else:
        register_form = RegistrationForm()
        profile_form = UserProfileForm()
        return render(request, 'acount/register.html', {'form': register_form, 'profile': profile_form})
