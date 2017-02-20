#***********************************************
#
#      Filename: peony/controlls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:28:18
# Last Modified: 2017-02-16 15:28:18
#**********************************************/

from django.http import HttpResponse,JsonResponse, Http404 
from django.core import serializers
from .models import User, Item
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

   
def record(request):
    print(dir(request.body))
    print(request.POST)
    return JsonResponse({"code":"aa"})
    
