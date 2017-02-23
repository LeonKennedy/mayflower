#***********************************************
#
#      Filename: peony/middleware.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-23 14:52:23
# Last Modified: 2017-02-23 14:52:24
#**********************************************/



class VerifyMiddleware(object):

    def __init__(self, get_response = None):
        self.get_response = get_response

    def __call__(self, request):
        response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        response = self.process_response(request, response)
        return response

    def process_request(self, request):
        print("here is request process")


    def process_response(self, request, response):
        print("here is response")
        return response


