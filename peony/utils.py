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

def get_item_info_from_xxx_api(barcode):
    iteminfo = {'name':'aaa', 'en_name':'aAa', 'price' : \
    12313.12, 'img':'https/image.quchu.co/23131','tag': \
    'bbbb', 'message': '哈哈哈哈'}
    return iteminfo


def json_parse(data):
    for k,v in data:
        if(isinstance(v,(tuple, dict, list))):
            print(1)
        elif(isinstance(v, models.Model)):
            print(2)
            





    
