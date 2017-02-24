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
        print("here is request process")


    def process_response(self, request, response):
        print("here is response")
        return response


    def verifytoken(self, request):
        mayflowertoken = request.META.get("mayflower")
        print(request.path)
        print(request.path_info)
        #print(request.content_params)
        if not mayflowertoken:
            return False

        t = Token.objects.get(pk  = mayflowertoken)
        return t.user
        


