from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.db.models import Count

def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    if request.POST['pw'] != request.POST['c_pw']:
        messages.error(request, "Passwords does not match")
        return redirect('/') 
    postData = {
    'f_n': request.POST['f_n'],
    'l_n': request.POST['l_n'],
    'eml': request.POST['eml'],
    'pw': request.POST['pw'],
    }
    result = User.objects.register(postData)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result[1].id
        return redirect('/') 

def login(request):
    postData = {
    'eml': request.POST['eml'],
    'pw': request.POST['pw'],
    }
    result = User.objects.login(postData)
    if result[0] == False:
        for error in result[1]:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['user_id'] = result[1].id
        return redirect('/')

def logout(request):
    request.session['user_id'] = None
    return redirect('/')
