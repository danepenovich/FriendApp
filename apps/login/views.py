# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import User

def logout(request):
    request.session.flush() #this is required to log the user out
    return redirect('/')

def index(request):
    return render(request, "login/index.html")

def register(request):
    results = User.objects.registerVal(request.POST)
    if results['status'] == False: #This is checking out validation from the models manager. As long as no issues were hit (which would set status to True) then our user will be succesfully registed.
        User.objects.createUser(request.POST)
        messages.success(request, "Account has been successfully created.")
    else:
        for error in results['errors']:
            messages.error(request, error) #If any issues get hit from our validation function in the manager, this will cause a specific error message on the page.

    return redirect('/')

def login(request):
    results = User.objects.loginVal(request.POST)
    if results['status'] == True:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/')
    else:
        request.session['name'] = results['user'].name
        request.session['id'] = results['user'].id
        request.session['email'] = results['user'].email
        return redirect('/dashboard')