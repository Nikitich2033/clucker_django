from django.shortcuts import render, redirect
from .models import User
from .forms import SignUpForm,LogInForm,PostForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
# Create your views here.

def log_in(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
            #Add error message here
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
    form = LogInForm()
    return render(request,'log_in.html', {'form':form})

def user_list(request):

    userList = User.objects.all();
    context= {'userList': userList}
    return render(request,'user_list.html',context)

def show_user(request,user_id):
    # if request.method == 'GET':
    # add context with content 
    return render(request,'show_user.html')

def feed(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.get(text)
    form = PostForm()
    return render(request,'feed.html',{'form':form})

def log_out(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request,'home.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = SignUpForm()
    return render(request,'sign_up.html',{'form':form})
