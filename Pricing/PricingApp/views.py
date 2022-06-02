from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import requests
import re
from API import utils
from django.http import JsonResponse
# Create your views here.

def index(request):
    return render(request,'Index.html')


def Admin(request):
    return render(request,'Admin.html')

def Driver(request):
    return render(request,'Driver.html')

def User(request):
    return render(request,'User.html')