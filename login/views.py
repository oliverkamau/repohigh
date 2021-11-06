from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

import json
# Create your views here.
from django.views.decorators.http import require_http_methods


def login(request):
     return render(request, 'login/login.html')

@require_http_methods(["POST"])
def login_view(request):
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
    else:
        messages.info(request, 'Invalid Login Credentials')
        return redirect('loginpage')
    # body = json.loads(request.body.decode())
    # user = authenticate(request, username=body["user_username"], password=body["user_password"])
    user = authenticate(username=username, password=password)
    if user is not None:
        auth.login(request,user)
        return redirect("/")
    else:
        messages.info(request,'Invalid Login Credentials')
        return redirect('loginpage')

def logout(request):
    auth.logout(request)
    return redirect('loginpage')