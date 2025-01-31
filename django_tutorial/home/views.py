from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required(login_url='signin')
@never_cache
def home1(request):
    return render(request,'home1.html')

def signup(request):
    if request.method == "POST":
        #usernmae = requst.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "user name already exist! please enther other username")
            return redirect('signup')

        if User.objects.filter(email=email):
            messages.error(request, "email already registered!")
            return redirect('signup')

        if pass1 !=pass2:
            messages.error(request, "password didn't match")
            return redirect('signup')
        
        

        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "your account has been successfully created")
        return redirect('signin')

    return render(request,'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, f"Welcome back, {fname}!")
            return redirect('home1')
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('signin')

    return render(request, 'signin.html')




def signout(request):
    logout(request)
    messages.success(request, "loged out successfully!")
    return redirect('signin') 
    