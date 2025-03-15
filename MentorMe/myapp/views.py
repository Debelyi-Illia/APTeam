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
from django.contrib.auth import login

# Create your views here.
def showDemoPage(request):
    return render(request, "demo.html")

def showHomePage(request):
    if request.user.is_authenticated:
        return render(request, "home_after_login.html")
    return render(request, "home.html") 

def LoginView(request):
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def RegisterView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print(f"Користувач {user.username} успішно зареєстрований!")  # Повідомлення про успіх
            return redirect('home')  # Перенаправлення на головну сторінку після реєстрації
        else:
            print("Помилки валідації форми:")  # Виведення помилок валідації
            for field, errors in form.errors.items():
                print(f"Поле {field}: {', '.join(errors)}")  # Виведення помилок для кожного поля
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def UserView(request):
    return render(request, 'user_profile.html')
