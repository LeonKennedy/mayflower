#***********************************************
#
#      Filename: peony/controlls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:28:18
# Last Modified: 2017-02-16 15:28:18
#**********************************************/

import pickle
from django.http import HttpResponse,JsonResponse, Http404 
from django.core import serializers
from django.conf import settings
from .models import User, Item, Account
from .utils import get_item_info_from_xxx_api
def register(request):
    if request.method == 'POST':
        phone = reqeust.POST['phone']
        wechatid = request.POST['signature']
        return JsonResponse({"code":"aa"})
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

def getItemInfo(request, barcode):
    #get from db
    items = Item.objects.filter(bar_code = barcode)
    if(items):
        item = items[0]
        return JsonResponse(item.getDict())

    #get from api
    iteminfo = get_item_info_from_xxx_api(barcode)
    if(iteminfo):
        i = Item(bar_code = barcode)
        i.dictializer(iteminfo)
        i.save()
        return JsonResponse(iteminfo)
    else:
        raise Http404()

   
#记录一条
def record(request, recordid):
    if(request.method == 'DELETE'):
        if(settings.DEBUG):
            Account.objects.filter(pk= recordid).delete()
            return JsonResponse({"success":True})
        else:
            Account.objects.filter(pk= recordid).update(status=7)
            return JsonResponse({"success":True})
    elif(request.method == 'GET'):
        a = Account.objects.filter(pk=recordid)
        if(a):
            return JsonResponse(a[0].getDict())
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
            return JsonResponse(a.getDict())
        return JsonResponse({"success":False})

#账户信息
def account(request):
    return JsonResponse({"success":False})
    

