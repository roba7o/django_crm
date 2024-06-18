from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def home(request):
    #Check to see if logging in (POST)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in successfully")
            return redirect('home')
        else:
            messages.success(request, "There was an error logging in, try again...")
            return redirect('home')
    else:
        return render(request, 'website/home.html', {}) 


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out mate")
    return redirect('home')