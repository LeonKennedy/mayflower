#***********************************************
#
#      Filename: test_main.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-03-09 22:28:42
# Last Modified: 2017-03-09 22:28:42
#**********************************************/


from django.test import TestCase
from peony.models import Account
import requests, json, pdb

class MainTestCase(TestCase):
    prehost = 'http://localhost:7900/peony'
    u = None
    headers = dict()
    def test_02_getProfile(self):
        url = '%s/profile' % self.prehost
        print("beging get profile....")
        r = requests.get(url, headers=self.headers)
        pdb.set_trace()
        dicr = json.loads(r.content)
        print(dicr)

    def test_01_register(self):
        url = '%s/login' % self.prehost
        data = {'deviceid':'test001'}
        print("beging logging.....")
        r = requests.post(url,data=data)
        dicr= json.loads(r.content)
        self.uid = dicr['data']['id']
        token = dicr['data']['token']
        self.headers['token'] = token
        pdb.set_trace()
        print(dicr)

    def cleandb(self):
        pass
