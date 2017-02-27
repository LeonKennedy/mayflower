#***********************************************
#
#      Filename: peony/controlls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:28:18
# Last Modified: 2017-02-16 15:28:18
#**********************************************/

import pickle, random, datetime
from django.http import HttpResponse,JsonResponse, Http404 
from django.core import serializers
from django.conf import settings
from .models import User, Item, Account, Captcha
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
            return resp()
        else:
            return resp(code=5126)
    raise Http404()
    


def register(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        wechatid = request.POST['signature']
        return resp()
    else:
        raise Http404("Question does not exist")

def profile(request, sign):
    u = User.objects.filter(signature=sign)
    if(u):
        if(request.method == 'POST'):
            u[0].phone = request.POST.get('phone')
            u[0].save()
    else:
        if(request.method == 'GET'):
            u = (User.objects.create(signature = sign),)
        elif(request.method == 'POST'):
            raise Http404()
    return JsonResponse(u[0].getDict())

def itemInfo(request, barcode):
    #get from db
    items = Item.objects.filter(bar_code = barcode)
    if(items):
        item = items[0]
        return resp(data=item.getDict())

    #get from api
    iteminfo = get_item_info_from_xxx_api(barcode)
    if(iteminfo):
        i = Item(bar_code = barcode)
        i.dictializer(iteminfo)
        i.save()
        return resp(data=iteminfo)
    else:
        raise Http404()

   
#记录一条
def record(request, recordid):
    if(request.method == 'DELETE'):
        if(settings.DEBUG):
            Account.objects.filter(pk= recordid).delete()
            return resp()
        else:
            Account.objects.filter(pk= recordid).update(status=7)
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

            # 检查item是否存在
            #if('item' == key):
            #    i = Item.objects.filter(pk = params[key])
            #    if(i):
            #        params[key] = i[0]
            #    else:
            #        del params[key]
                
        if(params):
            a = Account()
            a.dictializer(params)
            a.save()
            return resp(a.getDict())
        return resp()

#账户信息
def account(request):
    if(request.method == 'GET'):
        

        return resp()
    else:
        raise Http404()
    

