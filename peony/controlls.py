#***********************************************
#
#      Filename: peony/controlls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:28:18
# Last Modified: 2017-02-16 15:28:18
#**********************************************/

import pickle, random, datetime, pdb
from django.http import HttpResponse,JsonResponse, Http404 
from django.core import serializers
from django.conf import settings
from .models import User, Item, Account, Captcha,Token, Feedback, Sales
from .utils import get_item_info_from_xxx_api, resp, send_captcha


#发射手机验证码
def captcha(request):
    if(request.method == 'POST'):
        cap = random.randint(10000,99999)
        phone = request.POST['phone']
        if send_captcha(phone, cap):
            obj_c, created = Captcha.objects.update_or_create(phone = phone,defaults={'code':cap})
            return resp(data = cap)
        else:
            return resp(code = 5124)
    raise Http404()


def captcha_verify(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        cap = request.POST.get('captcha')
        if not phone or not cap:
            return resp(code = 5122)
        timedual = datetime.datetime.now() - datetime.timedelta(minutes=15)
        c = Captcha.objects.filter(phone=phone, code=cap, last_date__gte=timedual)
        if c:
            udict,created = register({'phone':phone})
            return resp(data=udict)
        else:
            return resp(code=5126)
    raise Http404()
    
def login(request):
    if request.method == 'POST':
        deviceid = request.POST.get('deviceid')
        if deviceid:
            udict , created = register({'device_id' : deviceid})
            print(created)
            return resp(data=udict)
    raise Http404()

def register(param):
    u, created =  User.objects.get_or_create(**param) 
    t, iscreated = Token.objects.get_or_create(user=u)
    data = u.getDict()
    data['token'] = t.id
    return data,created

def profile(request):
    u = request.META.get('user')
    if(request.method == 'POST'):
        u.phone = request.POST.get('phone')
        u.save()
    return resp(data = u.getDict())

def itemInfo(request, barcode):
    #get from db
    items = Item.objects.filter(bar_code = barcode)
    if(items):
        item = items[0]
        print(item.getDict())
        return resp(data=item.getDict())

    #get from api
    iteminfo = get_item_info_from_xxx_api(barcode)
    if(iteminfo):
        i = Item(bar_code = barcode)
        i.dictializer(dictionary = iteminfo)
        i.save()
        return resp(data=i.getDict())
    else:
        raise Http404()

   
#记录一条
def record(request, recordid):
    u = request.META.get('user')
    if(request.method == 'DELETE'):
        a = Account.objects.filter(pk= recordid,user=u)
        if a:
            a = a[0]
        if(settings.DEBUG):
            a.delete()
        else:
            a.update(status=7)
        #支出减少
        u.expenditure -= a.totelprice 
        u.save()
        return resp()
    elif(request.method == 'GET'):
        a = Account.objects.filter(pk=recordid)
        if(a):
            return resp(a[0].getDict())
        else:
            raise Http404()
    else:
        params = {}
        for key in request.POST:
            if(request.POST.get(key)):
                params[key] =  request.POST.get(key)
                
        if(params):
            a = Account()
            a.dictializer(dictionary = params)
            a.stock = params['num']
            a.user = u
            a.totelprice = (float(params['num']) * float(params['price'])) 
            a.save()
            #计算支出
            u.expenditure += a.totelprice
            u.save()
            return resp(a.getDict())
        return resp()

#账户信息
def account(request):
    if(request.method == 'GET'):
        u = request.META.get('user')
        try:
            offset = int(request.GET.get('offset',default=0))
            limit = int(request.GET.get('limit',default=10))
        except:
            offset, limit = 0, 10
        records = list()
        for a in Account.objects.filter(user=u)[offset:limit]:
            records.append(a.getDict())
        result = {
            'total' : Account.objects.filter(user = u).count(),
            'offset' : offset,
            'limit' : len(records),
            'data' : records}
        return resp(data = result)
    else:
        raise Http404()


def sale(request):
    u = request.META.get('user')
    account_id = request.POST.get('aid')
    num = float(request.POST.get('num'))
    a = Account.objects.get(pk=account_id, user=u)
    if a.stock < num:
        return resp(code=5211)
    a.stock -= num
    totalprice = request.POST.get('totalprice')
    if totalprice:
        u.income += float(totalprice)
    else:
        u.income += float(request.POST.get('price',deault=0)) * num
    s = Sales()
    s.dictializer(request.POST)
    


    
    #反馈
def feedback(request):
    u = request.META.get('user')
    if request.method == 'GET':
        try:
            offset = int(request.GET.get('offset',default=0))
            limit = int(request.GET.get('limit',default=10))
        except:
            offset, limit = 0, 10
        records = list()
        for f in Feedback.objects.filter(user=u)[offset:limit]:
            records.append(f.getDict())
        result = {
            'total' : Feedback.objects.filter(user = u).count(),
            'offset' : offset,
            'limit' : len(records),
            'data' : records}
        return resp(data = result)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content : f = Feedback.objects.create(user=u, content=content)
        return resp()
