#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: peony/barcode.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-03-20 14:44:50
# @Last Modified: 2017-03-20 14:44:50

import requests, time, pdb
from bs4 import BeautifulSoup

BARCODE_TABLE = (
(0,19,'American', 'us'),
(30,39, 'us'),
(60,139, 'us'),
(450,459, 'jp'),
(490,499, 'jp'))

class BarCode:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    def __init__(self, barcode):
        self.code = barcode
        self.s = requests.Session()

    def search_yahoo(self):
        url = 'http://shopping.yahoo.co.jp/search'
        params = { 'p' : self.code,
            'ei': 'UTF-8',
            'first' : 1, 
            'ss_first': 1,
            'ts' : int(time.time())}
        r = requests.get(url, params = params, headers=self.headers)
        bs = BeautifulSoup(r.content, 'lxml')
        item = bs.find('li', attrs={'data-item-pos':True})
        pdb.set_trace()
        return {
            'img' : item.find('dt').img['src'],
            'name' : item.find('dd', class_ = 'elName').get_text().encode('utf-8'),
            'price' : round(int(item.find('dd', class_='elPrice').span.get_text()) * 0.0612),
            'seller' : item.find('span', class_ = 'elSeller').find_next('span').get_text().encode('utf8'),
            'bar_code' : self.code}


    @staticmethod
    def search_taobaoh5(barcode):
        url = "http://h5.m.taobao.com/qrbuy/sdk.html"
        params = {
            'appkey' : 23040383,
            'barcode' : barcode,
            'type' : 1 }
        r = requests.get(url, params = params, headers = self.headers)

if __name__ == "__main__":
    b =  BarCode(4987084410443)
    print(b.search())

