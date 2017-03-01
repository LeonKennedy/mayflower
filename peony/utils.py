#***********************************************
#
#      Filename: peony/utils.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-20 10:51:42
# Last Modified: 2017-02-20 10:51:42
#**********************************************/

from django.db import models
from django.http import HttpResponse,JsonResponse, Http404 
import hashlib, random

def get_item_info_from_xxx_api(barcode):
    iteminfo = {'name':'妮维雅小黑瓶', 'en_name':'black bottle', 
    'price' :  12313.12,
    'img':'https://ss1.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1488375832&di=b876ca7f1010d2b08c49e34a75b7111f&src=http://image1.suning.cn/b3c/catentries/000000000121293197_1_800x800.jpg',
    'netweight':1000,
    'tag': 'bbbb', 'message': '眼霜 效果不错'}
    return iteminfo


def json_parse(data):
    for k,v in data:
        if(isinstance(v,(tuple, dict, list))):
            print(1)
        elif(isinstance(v, models.Model)):
            print(2)
            

#返回接口
def resp(success=True, data=None, code = 0):
    error_code = {
#       验证码填写时缺少参数
        5122: 'verify captcha code miss phone number and captcha code',
        5124: 'captcha server is wrong! calling olenji!',
        5126: 'captcha is not matching!',
        5128: 'captcha is expired! please re-send!',
        
    }
    answer = {"success":success, "data":data, "code":code, "msg":error_code.get(code)}
    if code:
        answer['success'] = False

    return JsonResponse(answer)


def md5(p):
    m = hashlib.md5()
    m.update(p)
    return m.hexdigest()




def send_captcha(phone, captcha):
    return True
    






    
