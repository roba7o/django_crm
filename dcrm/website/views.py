from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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


def customer_record(request, pk):
    if request.user.is_authenticated:
        #Look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'website/record.html', {'customer_record':customer_record}) 
    else:

        messages.success(request, "You must be logged in to view that page")
        return redirect('home')
    
def delete_record(request, pk):
    
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record deleted successfully")
        return redirect('home')
    else:

        messages.success(request, "You must be logged in to delete Record")
        return redirect('home')

def add_record(request):
        form = AddRecordForm(request.POST or None)
        if request.user.is_authenticated:
            if request.method == "POST":
                if form.is_valid():
                    add_record = form.save()
                    messages.success(request, "Record Added...")
                    return redirect('home')
            return render(request, 'website/add_record.html', {'form':form})
        else:
            messages.success(request, "You must be logged in to do that...")
            return render('home') 

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record is updated...")
            return redirect('home')

        return render(request, 'website/update_record.html', {'form':form})
    
    else:
        messages.success(request, "You must be logged in to do that...")
        return redirect('home')