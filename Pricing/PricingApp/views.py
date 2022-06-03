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
    #UpdatePrice
    if request.method == "POST" and request.POST.get('req') == 'UpdatePrice':
        print('Inside Update Price')
        url = utils.makeup_url('pricingModule.py')
        print(url)
        payload = {'req':'updatePrice','type':request.POST.get('type'),'price':request.POST.get('price')}
        print(payload)
        priceres = requests.post(url,data = payload).json()
        return JsonResponse({'data':priceres},status=200)
    
    url = utils.makeup_url('pricingModule.py')
    payload = {'req':'getPrice'}
    price = requests.post(url,data = payload).json()
    return render(request,'Admin.html',{'price':price})

def Driver(request):
    if request.method == "POST" and 'generatebill' in request.POST:
        print('Inside generatebill')
        url = utils.makeup_url('pricingModule.py')
        payload = {'req':'clculatePrice','name':request.POST.get('Pname'),'distance':request.POST.get('Tdistance'),'time':request.POST.get('Ttime')}
        print(payload)
        response = requests.post(url,data=payload).json()
        if response['response']:
            return redirect('user',travelid=response['travalID'])
        else:
            return render(request,'Driver.html',{'iserror':True,'errmsg':'Error in generate bill'})
        
        
    return render(request,'Driver.html',{'iserror':False,'errmsg':'NA'})

def User(request,travelid=None):
    url = utils.makeup_url('pricingModule.py')
    payload = {'req':'getDetails','travalID':travelid}
    print(payload)
    response = requests.post(url,data=payload).json()
    bill={}
    bill['travelid']=response['travalID']
    bill['name']=response['name']
    bill['time']=response['time']
    bill['distance']=response['distance']
    bill['totalprice']=response['totalPrice']
    return render(request,'User.html',{'bill':bill})