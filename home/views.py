from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import os
from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_django
from home.models import UserCreationForm
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required   
from django.contrib.auth.decorators import permission_required
from rolepermissions.roles import assign_role
from rolepermissions.decorators import has_role_decorator
from .forms import ImageUploadForm
from .models import Image
import boto3

@login_required(login_url="login")
@has_role_decorator('noivos')
def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ImageUploadForm()

    return render(request, 'home.html', {'form': form})


@login_required(login_url="login")
def galeria(request):
    images = Image.objects.all()
    return render(request, "galeria.html", {'images': images})

    

def signin (request):
   if request.user.is_authenticated:
       return redirect('view_images')
   if request.method == "GET":
      return render (request,"login.html")
   else:
      username = request.POST.get('username')
      password = request.POST.get('password1')

      user = authenticate(username=username, password=password)
      if user:
       login_django(request, user)
       return redirect ('view_images')
         
      #    return redirect ('home')
   return render (request, "login.html")
    


    
def register(request):
    if request.user.is_authenticated:
       return redirect('galeria')
    if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          username = form.cleaned_data.get("username")
          password = form.cleaned_data.get("password1")
          email = form.cleaned_data.get("email")
          is_superuser = form.cleaned_data.get("is_superuser")
          if User.objects.filter(email=email).exists():
             print ("exists")
             return
         #  user = User(username=username, password=password, email=email)
         #  login_django(request, user)
          user2 = User.objects.create_user(username=username, password=password, email=email, is_superuser=is_superuser)
          if is_superuser == 1:
             assign_role(user2, 'noivos')
          user2.save()
          return redirect ('login') 
       else:
          return render(request, 'register.html') 
    else:
      form = UserCreationForm()
      return render(request, 'register.html')
     



def index (request):
   return render (request, "index.html")




def sair(request):
   logout(request)
   return redirect('login')




def testes (request):

   return render(request, "testes.html")



    
    
 