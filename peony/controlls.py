#***********************************************
#
#      Filename: peony/controlls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:28:18
# Last Modified: 2017-02-16 15:28:18
#**********************************************/

import pickle, random, datetime, pdb, re
from django.http import HttpResponse,JsonResponse, Http404 
from django.core import serializers
from django.conf import settings
from django.db import transaction
from .models import User, Item, Account, Captcha,Token, Feedback, Sales, Inventory
from .utils import get_item_info_from_xxx_api, resp, send_captcha
from .barcode import BarCode


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
    data = u.getBaseDict()
    data['token'] = t.id
    return data,created

def profile(request):
    u = request.META.get('user')
    if(request.method == 'POST'):
        u.phone = request.POST.get('phone')
        u.save()
    return resp(data = u.getBaseDict())

def itemInfo(request, barcode):
    #get from db
    u = request.META.get('user')
    if not re.match(r'\d{13}', barcode):
        return resp(code=2231)

    items = Item.objects.filter(bar_code = barcode)
    if(items):
        momitem = None
        for item in items:
            if item.user == u:
                return resp(data=item.getBaseDict())
            if not item.mom:
                momitem = item
        #新建一个副本
        ibyu = Item()
        ibyu.itemcopy(momitem)
        ibyu.user = u
        ibyu.mom = momitem
        ibyu.save()
        return resp(data=ibyu.getBaseDict())
                
    #get from api
    iteminfo = BarCode.search_h5taobao(barcode)
    if(iteminfo):
        i = Item(bar_code = barcode)
        i.dictializer(dictionary = iteminfo)
        i.save()
        ibyu = Item()
        ibyu.itemcopy(i)
        ibyu.user = u
        ibyu.mom = i
        ibyu.save()
        return resp(data=ibyu.getBaseDict())
    else:
        raise Http404()


def records(request, invid):
    if request.method == 'GET':
        u = request.META.get('user')
        if invid:
            a = Account.objects.filter(user = u, inventory_id = invid)
        else:
            a = Account.objects.filter(user = u)
        results = list()
        for la in a:
            results.append(la.getBaseDict())
        return resp(data=results)
    
   
#记录一条
@transaction.atomic
def record(request, recordid):
    u = request.META.get('user')
    if(request.method == 'DELETE'):
        a = Account.objects.filter(pk= recordid,user=u, status=0)
        if a:
            a = a[0]
        else:
            return resp(success=False)
        if(settings.DEBUG):
            a.delete()
        else:
            a.update(status=7)
        #inv = Inventory.objects.get(user=u, item = a.item,)
        inv = a.inventory
        inv.stock -= a.num
        inv.num -= a.num
        inv.expences -= a.totalprice
        inv.save()
        #支出减少
        u.expenditure -= a.totalprice 
        u.save()
        return resp()
    elif(request.method == 'GET'):
        a = Account.objects.filter(pk=recordid, user =u)
        if(a):
            return resp(a[0].getBaseDict())
        else:
            raise Http404()
    elif(request.method == 'POST'):
        a = Account(user = u)
        a.dictializer(queryset=request.POST)
        a.save()
        #inv_id = int(request.POST.get('inventory_id', default = 0))
        inv, created = Inventory.objects.get_or_create(user=u, item=a.item)
        num = float(request.POST.get('num',default =0)) 
        totalprice = float(request.POST.get('totalprice', default = 0))
        if created:
            inv.num = inv.stock = num
            inv.expences = totalprice
        else:
            inv.stock += num
            inv.num += num
            inv.expences += totalprice
        inv.save()
        a.inventory = inv
        a.save()
        return resp()
    '''
#    design by olenji
    elif(request.method == 'POST'):
        a = Account(user = u)
        a.dictializer(queryset=request.POST)
        a.save()
        inv_id = int(request.POST.get('inventory_id', default = 0))
        inv = Inventory.objects.filter(pk = inv_id, user = u) 
        if inv:
            inv = inv[0]
        else:
            inv = Inventory(user= u, item = a.item)
            inv.save()
            a.inventory = inv
            a.save()
        inv.stock += float(a.num)
        inv.num += float(a.num)
        inv.expences += float(a.totalprice)
        inv.save()
        u.expenditure += float(a.totalprice)
        u.save()
        return resp()
        '''

#库存信息
def inventory(request):
    u = request.META.get('user')
    if request.method == 'GET':
        return resp()
    else:
        raise Http404()

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
            records.append(a.getBaseDict())
        result = {
            'total' : Account.objects.filter(user = u).count(),
            'offset' : offset,
            'limit' : len(records),
            'data' : records}
        return resp(data = result)
    else:
        raise Http404()


@transaction.atomic
def sale(request, sid):
    u = request.META.get('user')
    if request.method == 'GET':
        s = Sales.objects.get(user = u, pk = sid)
        return resp(data=s.getBaseDict())
    elif request.method == 'DELETE':
        s = Sales.objects.get(pk = sid, user = u)
        #订单修改
        inv = s.inventory
        if(settings.DEBUG):
            s.delete()
        else:
            s.status = 7
            s.save()
        inv.income -=s.totalprice
        inv.save()
        u.income -= s.totalprice
        u.save
        return resp()
    elif request.method == 'POST':
        try:
            inv_id = int(request.POST['inventory_id'])
            inv = Inventory.objects.get(pk = inv_id, user = u)
        except ValueError:
            return resp(code=2222)
        except :
            return resp(code=5214)
        num = float(request.POST['num'])
        totalprice = float(request.POST['totalprice'])
        if inv.stock < num:
            return resp(code=5213)
        s = Sales(user=u, item=inv.item,num = num, totalprice = totalprice)
        s.price = request.POST['price']
        s.message = request.POST.get('message')
        s.save()
        inv.stock -= num
        inv.income += totalprice
        inv.save()
        u.income += totalprice
        u.save()
        return resp(data = s.getBaseDict())

@transaction.atomic
def sales(request):
    u = request.META.get('user')
    if request.method == 'GET':
        s = Sales.objects.filter(user = u)
        return resp()
    elif request.method == 'DELETE':
        s = Sales.objects.get(pk = sid, user = u)
        if(settings.DEBUG):
            s.delete()
        else:
            s.update(status=7)
    else:
        try:
            inv_id = int(request.POST['invid'])
            inv = Inventory.objects.get(pk = inv_id, user = u)
        except ValueError:
            return resp(code=2222)
        except :
            return resp(code=5214)
        num = float(request.POST['num'])
        totalprice = float(request.POST['totalprice'])
        if inv.stock < num:
            return resp(code=5213)
        s = Sales(user=u, item=inv.item,num = num, totalprice = totalprice)
        s.price = request.POST['price']
        s.message = request.POST.get('message')
        s.save()
        inv.stock -= num
        inv.income += totalprice
        inv.save()
        u.income += totalprice
        u.save()
        return resp(data = s.getBaseDict())

    
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
            records.append(f.getBaseDict())
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
