from __future__ import unicode_literals
from django.db import models
import bcrypt 
#import datetime module
from datetime import datetime, timedelta
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
#format regex 
import re 
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
# EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
#name validation
        if len(postData['name']) < 1:
            errors['name']="Name must be at least 3 characters long"
        if bool(re.search(r'\d', postData["name"])):
            errors['name']= "Name must be letters only"
#username validation
        if len(postData['username'])<1:
            errors['username'] = "please provide a user name"
#datehired 
        # try: 
        if datetime.strptime(postData['datehired'], "%Y-%m-%d") > datetime.today():
            errors['datehired']="Hire date can not be in the future"
        if datetime.strptime(postData["datehired"], "%Y-%m-%d") == False:
            errors['datehired'] = "Hire date can not be left blank"
        # except ValueError:
        #         errors['datehired'] = "Hire date not valid"
#password 
        if len(postData['password']) < 1:
            errors['password'] = "Password must not be blank!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
#confirm password
        if postData['password']!=postData["confirm_password"]:
            errors['password'] = "Password does not match confirmation"
#return errors for looping in html
        return errors        

    def login_val(self, postData):
        errors = {}  
        user = User.objects.filter(username=postData['username'])
        print user
        if len(postData['username']) < 1:
            errors['username'] = "Please enter your user name"
        if len(postData['password'])<1:
            errors['password'] = "Please enter a password"
        if not user:
            errors['username'] = "Incorrect login"
        #if password-entered hash doesn't match the database hash
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['username'] = "Incorrect login"
        return errors 

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length= 255)
    password = models.CharField(max_length=255)
    datehired = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return "name: " + self.name + ", username: " + self.username 

class ItemManager(models.Manager):
    def item_val(self, postData):
        user = User.objects.filter()
        errors = []
        if len(postData['new_item'])<1:
            errors.append("field can not be left empty")
        if len(postData['new_item']) < 3:
            errors.append("field must be atleast 3 characters long")
        return errors
#item should appear on the wisher's table after being added --> views & html
class Item(models.Model):
    item = models.CharField(max_length=255)
    wished_by = models.ManyToManyField(User, related_name = "wish_for")
    added_by = models.ForeignKey(User, related_name="addeditem", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()
    def __str__(self):
        return self.item 