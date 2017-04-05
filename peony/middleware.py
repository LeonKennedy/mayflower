#***********************************************
#
#      Filename: peony/middleware.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-23 14:52:23
# Last Modified: 2017-02-23 14:52:24
#**********************************************/

from .models import Token
from django.http import HttpResponse,JsonResponse, Http404 
import re,pdb


class VerifyMiddleware(object):

    def __init__(self, get_response = None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)

        if not self.verifytoken(request):
            raise Http404("token is wrong")
        
        if not response:
            response = self.get_response(request)
        #response = self.process_response(request, response)
        return response

    def process_request(self, request):
        pass


    def process_response(self, request, response):
        print("here is response")
        return response


    def verifytoken(self, request):
        #需要验证的方法 加入此元祖
        repr_list = ('sale', 'inventory', 'profile','item','record', 'records', 'account','feedback')
        mayflowertoken = request.META.get("HTTP_TOKEN")
        if not request.path.split('/')[2] in repr_list:
            return True
        if not mayflowertoken:
            raise Http404()

        try:
            t = Token.objects.get(pk  = mayflowertoken)
            request.META.setdefault('user',t.user)
        except:
            raise Http404()

        return t.user
        


