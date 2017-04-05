#!/usr/bin/env python
#-*- coding: utf-8 -*-
# @Filename: exchangerate.py
# @Author: olenji - lionhe0119@hotmail.com
# @Description: ---
# @Create: 2017-04-05 15:33:59
# @Last Modified: 2017-04-05 15:33:59
#
import requests, pdb
from bs4 import BeautifulSoup
class RateSpider:
    
    ChinaBankUrl = (
        'http://www.boc.cn/sourcedb/whpj/enindex.html',)
        #'http://www.boc.cn/sourcedb/whpj/enindex_2.html',
        #'http://www.boc.cn/sourcedb/whpj/enindex_3.html',
        #'http://www.boc.cn/sourcedb/whpj/enindex_4.html', )

    ratetable = list()
    countries = list()
    def getRateRecords(self, url):
        r = requests.get(url)
        bs = BeautifulSoup(r.content, 'lxml')
        item = bs.find('table', attrs = {"bgcolor" :"#EAEAEA"})
        trset = item.find_all('tr')
        for tr in trset:
            tds = tr.find_all('td')
            if tds:
                record = dict()
                record['publish_date'] = tds.pop().text.replace('\xa0\n\t\t' , ' ')

                record['middle_rate'] = self._float(tds) 
                record['cash_sell_rate'] = self._float(tds)
                record['sell_rate'] = self._float(tds)
                record['cash_buy_rate'] = self._float(tds)
                record['buy_rate'] = self._float(tds)
                record['name'] = tds.pop().text
                self.uniqueAppend(record)

    def getAllPage(self):
        for url in self.ChinaBankUrl:
            self.getRateRecords(url)

    def uniqueAppend(self, record):
        if record['name'] in self.countries:
            return False
        else:
            self.countries.append(record['name'])
            self.ratetable.append(record)

    def _float(self, tds):
        a  = tds.pop().text
        return float(a) if a else None
                


if __name__ == "__main__":
    r = RateSpider()
    url = 'http://www.boc.cn/sourcedb/whpj/enindex.html'
    r.getAllPage()
    print(r.ratetable)
    print(len(r.ratetable))

