#***********************************************
#
#      Filename: peony/urls.py
#
#        Author: olenji - lionhe0119@hotmail.com
#   Description: ---
#        Create: 2017-02-16 15:23:11
# Last Modified: 2017-02-16 15:23:11
#**********************************************/

from django.conf.urls import url
from . import controlls

app_name = 'peony'
urlpatterns = [
    url(r'^register$', controlls.register, name='register'),
    url(r'^profile/(?P<sign>[0-9,a-z]+)$',controlls.profile, name='profile'),
    url(r'^getiteminfo/(?P<barcode>[A-Za-z0-9]+)$', controlls.getItemInfo, name='iteminfo'),
    url(r'^record$', controlls.record, name= 'record'),
]

