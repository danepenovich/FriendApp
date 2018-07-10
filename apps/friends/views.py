# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from ..login.models import User

def dashboard(request):
    otherusers = User.objects.exclude(id = request.session['id']).difference(User.objects.get(id = request.session['id']).friend.all())
    
    #Here is a longer way to do the above code:

    # people = User.objects.exclude(id = request.session['id'])
    # myperson = User.objects.get(id = request.session['id'])
    # unrelated = []
    # for user in people:
    #     if user not in myperson.friend.all():
    #         unrelated.append(user)

    context = {
        'user': User.objects.get(id = request.session['id']),
        'user2': otherusers
    }
    if 'name' not in request.session:
        return redirect('/') #All important routes that users shouldn't be able to access without being logged in should have this line!!!!!

    return render(request, "friends/dashboard.html", context)

def showUser(request, id):
    context = {
        'user': User.objects.get(id = id),
    }
    if 'name' not in request.session:
        return redirect('/')

    return render(request, "friends/user.html", context)

def addFriend(request, id):
    if 'name' not in request.session:
        return redirect('/')
    u1 = User.objects.get(id = request.session['id'])
    u1.friend.add(User.objects.get(id = id))
    messages.success(request, 'Friend added.')
    return redirect('/dashboard')

def removeFriend(request, id):
    if 'name' not in request.session:
        return redirect('/')
    u1 = User.objects.get(id = request.session['id'])
    u1.friend.remove(User.objects.get(id = id))
    messages.success(request, 'Friend removed.')
    return redirect('/dashboard')