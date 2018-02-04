from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
from .models import User
from django.contrib import messages
import bcrypt
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'wishapp/index.html')

def registration(request):
    errors = User.objects.reg_val(request.POST)
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="reg {}".format(key))
        return redirect('/')
    else:
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], datehired=datetime.strptime(request.POST["datehired"], "%Y-%m-%d"), password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
        request.session['id'] = user.id
        return redirect('/home')
    
def login(request):
    errors = User.objects.login_val(request.POST)
    print errors
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="log {}".format(key))
        return redirect("/")
    else:
        request.session["id"]=User.objects.get(username=request.POST['username']).id
        # messages.success(request, "Welcome!")
        return redirect("/home")
    return errors

def logout(request):
    this_user = request.session['id']
    request.session.flush()
    return redirect('/')

def home(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')
    

    user_logged = User.objects.get(id= request.session['id'])
    
    my_add = Item.objects.filter(added_by__id = request.session['id'])
    my_wished = Item.objects.filter(wished_by__id = request.session['id'])
    others_wished = Item.objects.all().exclude(wished_by =request.session['id'])

    context = {
        "user_logged" : user_logged,
        "my_add" : my_add,
        "my_wished" : my_wished,
        "others_wished" : others_wished,
    }

    return render(request, "wishapp/home.html", context)

def create_page(request):
    return render(request, "wishapp/create.html")

def create(request): #create route processing of "new_word"
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

    user_logged = User.objects.get(id= request.session['id'])
    print user_logged
    print "******"
    errors = Item.objects.item_val(request.POST)
    # print errors
    if len(errors):
        for error in errors.iteritems():
            messages.error(request, error)
        return redirect("/create")
    else:
        try:
            item = Item.objects.get(item= request.postData['new_item'])
        except: 
            new_item = Item.objects.create(item = request.POST['new_item'], added_by= user_logged)
        return redirect('/home')
    # print errors 
    return render(request, "wishapp/create.html", context)
       
def delete(request, id):
    destroy = Item.objects.get(id=id)
    destroy.delete() 
    return redirect('/home')

def addwish(request, id):
    this_item = Item.objects.get(id=id)
    this_item.wished_by.add(request.session['id'])
    return redirect('/home')

def removewish(request, id):
    user_logged = User.objects.get(id= request.session['id'])
    item = user_logged.wish_for.get(id=id)
    item.wished_by.remove(user_logged)
#.remove() must be passed an argument and will only dissolve the many to many.
#.delete() deletes the object preceeding it and completely deletes from db. 
    return redirect('/home')

def wish_item(request, id):
    wish_item = Item.objects.get(id =id)
    users_wishing = wish_item.wished_by.all()
    context = {
        "wish_item" : wish_item,
        "users_wishing" : users_wishing
    }
    return render(request, "wishapp/wish_item.html", context)