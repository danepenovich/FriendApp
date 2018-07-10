# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import re
import bcrypt

email_regex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
name_regex = re.compile(r'^[A-Za-z]\w+$')
alias_regex = re.compile(r'[A-Za-z0-9]')
password_regex = re.compile(r'[A-Za-z0-9@#$%^&+=]{6,}')
dob_regex = re.compile(r'^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$')

class UserManager(models.Manager):
    def loginVal(self, postData):
        results = {'errors':[], 'status': False, 'user': None}
        email_matches = self.filter(email = postData['email'])
        if len(email_matches) == 0:
            results['errors'].append('Incorrect email or password.')
            results['status'] = True
        else:
            results['user'] = email_matches[0]
            if not bcrypt.checkpw(postData['password'].encode(), results['user'].password.encode()):
                results['errors'].append('Incorrect email or password.')
                results['status'] = True
        return results

    def createUser(self, postData):
        password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        print password
        self.create(
            name = postData['name'],
            alias = postData['alias'],
            email = postData['email'],
            password = password,
            dob = postData['dob'])
   
    def registerVal(self, postData):
        results = {'errors':[], 'status': False}

        if len(postData['name']) < 2:
            results['status'] = True
            results['errors'].append('Name field cannot be under 3 characters.')

        if not re.match(name_regex, postData['name']):
            results['status'] = True
            results['errors'].append('Name field can only be letter characters.')

        if len(postData['alias']) < 2:
            results['status'] = True
            results['errors'].append('Alias field cannot be under 3 characters.')

        if not re.match(alias_regex, postData['alias']):
            results['status'] = True
            results['errors'].append('Alias field can only be alphanumeric characters.')

        if not re.match(email_regex, postData['email']):
            results['status'] = True
            results['errors'].append('Invalid email')

        if not re.match(password_regex, postData['password']):
            results['status'] = True
            results['errors'].append("Password cannot contain spaces or underscores and must be at least 6 characters.")

        if postData['password'] != postData['c_password']:
            results['status'] = True
            results['errors'].append('Passwords do not match.')

        if not re.match(dob_regex, postData['dob']):
            results['status'] = True
            results['errors'].append('Please insert your date of birth.')

        user = self.filter(email = postData['email'])
        
        if len(user) > 0:
            results['status'] = True
            results['errors'].append("That email is already in use.")

        return results

class User(models.Model):
    name = models.CharField(max_length = 50)
    alias = models.CharField(max_length = 50)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50)
    dob = models.DateField(auto_now=False, auto_now_add=False)
    friend = models.ManyToManyField("self", related_name = "friends")
    objects = UserManager()