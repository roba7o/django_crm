from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.

def home(request):
    records = Record.objects.all()


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
        return render(request, 'website/home.html', {'records':records}) 


def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "you have been logged out mate")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully logged in ")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'website/register.html', {'form':form}) 
        
    return render(request, 'website/register.html', {'form':form}) 