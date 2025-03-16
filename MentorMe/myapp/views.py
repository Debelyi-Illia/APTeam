from django.shortcuts import render,redirect, reverse

# Create your views here.
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")

def showHomePage(request):
    if request.user.is_authenticated:
        return render(request, "home_after_login.html")
    return render(request, "home.html") 

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('user_profile')
            else:
                form.add_error(None, "Невірний логін або пароль")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def RegisterView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.user_def_role = "Mentor"
            user.save()
            login(request, user)
            print(f"Користувач {user.username} успішно зареєстрований!")
            return redirect('user_profile')
        else:
            print("Помилки валідації форми:")
            for field, errors in form.errors.items():
                print(f"Поле {field}: {', '.join(errors)}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def UserView(request):
    return render(request, 'user_profile.html')

def custom_logout(request):
    logout(request)
    return redirect('home')

def search_users(request):
    query = request.GET.get('query', '')
    results = []

    if query:
        results = User.objects.filter(
            username__icontains=query
        ) | User.objects.filter(
            user_def_role__icontains=query
        )

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'home_after_login.html', context)

def AdView(request):
    if request.user.is_authenticated:
        return render(request, 'ad.html')
    else:
        return redirect('login')
