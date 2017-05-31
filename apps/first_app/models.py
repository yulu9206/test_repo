from __future__ import unicode_literals
from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX =re.compile('^[A-z]+$')

class UserManager(models.Manager):
  def login(self, postData):
    errors = []
    if User.objects.filter(eml=postData['eml']):
        db_pw = User.objects.get(eml=postData['eml']).pw.encode()
        form_pw = postData['pw'].encode('utf8')
        if not bcrypt.checkpw(form_pw, db_pw):
            errors.append('Password is incorret!')
            return [False, errors]
        else:
            user = User.objects.get(eml=postData['eml'])
            return [True, user] 
    else:
        errors.append('User does not exist!')
        return [False, errors]

  def register(self, postData):
    errors = []
    if len(postData['f_n']) == 0:
        errors.append('First name cannot be empty!')
    if len(postData['l_n']) == 0:
        errors.append('Last name cannot be empty!')
    if not EMAIL_REGEX.match(postData['eml']):
        errors.append('Email address is invalid!')
    if len(postData['pw']) < 8:
        errors.append('Passord is too short!')
    if User.objects.filter(eml=postData['eml']).first() != None:
        errors.append('Email address is already registered!')
    if errors != []:
        return [False, errors]
    else:
        user = User.objects.create(f_n=postData['f_n'], l_n=postData['l_n'], eml=postData['eml'], pw=bcrypt.hashpw(postData['pw'].encode('utf8'), bcrypt.gensalt()))
        return [True, user] 

class User(models.Model):
  f_n = models.CharField(max_length=38)
  l_n = models.CharField(max_length=38)
  eml = models.CharField(max_length=38)
  pw = models.CharField(max_length=38)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager()