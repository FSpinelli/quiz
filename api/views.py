# coding=utf8
# -*- coding: utf8 -*-
# vim: set fileencoding=utf8 :

import jwt
from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth import authenticate, login as auth_login, logout
from api.forms import *
from api.models import *
from django.utils.decorators import method_decorator
from decorators import *


def error_form_serialization(error_dict):  
    """  
    This method strips the proxy objects from the
    error dict and casts them to unicode. After
    that the error dict can and will be
    json-serialized.  
    """  
    plain_dict = dict([(k, [unicode(e) for e in v]) for k,v in error_dict.items()])   
    return simplejson.dumps(plain_dict)


@csrf_exempt
def index(request):
    return HttpResponse("epedidos api")

@csrf_exempt
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                token = jwt.encode({request.POST.get('username',False): request.POST.get('password',False)}, 'secret', algorithm='HS256')                
                return HttpResponse('{"token":"'+token+'"}')
            else:
                return HttpResponse('404') #usuario desativado

        else:
            return HttpResponse('400') #usuario ou senha incorreta

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        register_form = RegisterForm(data=request.POST)
        if register_form.is_valid():
            try:
                register = register_form.save()
                register.set_password(register.password)
                register.save()
                token = jwt.encode({request.POST.get('username',False): request.POST.get('password',False)}, 'secret', algorithm='HS256')
                return HttpResponse('{"token":"'+token+'"}')
            except:
                return HttpResponse('500')
        else:
            return HttpResponse(error_form_serialization(register_form.errors))

@is_auth
@csrf_exempt
def category(request):
    if request.method == 'GET':
        category = Category.objects.all()
        category_serializer = serializers.serialize("json", category)
        return HttpResponse(category_serializer)

@csrf_exempt
def user_category(request):
    if request.method == 'GET':
        u = User.objects.filter(pk=1)
        user_categories = UserCategory.objects.filter(user=u)
        user_categories_serializer = serializers.serialize("json", user_categories, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return HttpResponse(user_categories_serializer)