#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import urllib2 as url
import requests as req
import ast
from smb_logic import Logic
import json
import sys
import yaml
import ujson
import cookielib

log = Logic()

def decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = decode_list(item)
        elif isinstance(item, dict):
            item = decode_dict(item)
        rv.append(item)
    return rv

def decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = decode_list(value)
        elif isinstance(value, dict):
            value = decode_dict(value)
        rv[key] = value
    return rv

class SteamBotHttp:

    def __init__(self):
        self.host_normal = 'http://steamcommunity.com'
        self.host_https = 'https://steamcommunity.com'
        self.market = '/market'
        #currency=3 == euro
        self.item_price_viewer = '/priceoverview/?currency=3&appid=730&market_hash_name='
        self.recent_listed = '/recent/?country=PT&language=english&currency=3'
        self.complete_url_item = self.host_normal+self.market+self.item_price_viewer
        self.complete_url_recent = self.host_normal+self.market+self.recent_listed
        self.sell_item_url = self.host_https+self.market+'/sellitem/'
        self.buy_item_url_without_listingid = self.host_https+self.market+'/buylisting/'
        self.sess = ""
        self.headers_sell = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            "Host": "steamcommunity.com",
            #cookie
            "Referer": "https://steamcommunity.com/id/craked5/inventory",
            "Origin": "https://steamcommunity.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.headers_buy = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
        'Connection': 'keep-alive',
        'Content-Length': '83',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        #cookie
        'CSP':'active',
        'DNT':'1',
        'Host':'steamcommunity.com',
        'Origin':'http://steamcommunity.com',
        'Referer':'http://steamcommunity.com/market/listings/730/USP-S%20%7C%20Stainless%20%28Battle-Scarred%29',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
}

        #price = preco que eu quero receber = price+fee_price
        self.data_sell = {
            "sessionid" : self.sess,
            "appid" : 730,
            "contextid" : 2,
            "assetid" : 2624120824,
            "amount" : 1,
            "price" : 1000
        }
        #subtotal = price without fee
        #fee = a fee
        #total = price com a fee
        self.data_buy = {
            'sessionid': self.sess,
            'currency': 3,
            'subtotal': 0,
            'fee': 0,
            'total': 0,
            'quantity': 1
        }

    def urlQueryItem(self,item):
        steam_response = req.get(self.complete_url_item + item)
        item_temp = ujson.loads(steam_response.text)
        item_temp = decode_dict(item_temp)
        return item_temp

    def urlQueryRecent(self):
        try:
            steam_response = req.get(self.complete_url_recent)
        except req.ConnectionError:
            return False
        try:
            recent_temp = ujson.loads(steam_response.text)
        except ValueError:
            return False
        #recent_temp = decode_dict(recent_temp)
        return recent_temp

    #price = ao preco que eu quero receber
    def sellitem(self,assetid,price):
        price_temp = price * 100
        self.data_sell['assetid'] = int(assetid)
        self.data_sell['price'] = int(price_temp)
        print req.post(self.sell_item_url, data=self.data_sell, headers=self.headers_sell)

    def buyitem(self,listing,subtotal,fee,nome):
        temp_tuple = []
        self.data_buy['subtotal'] = int(subtotal)
        self.data_buy['fee'] = int(fee)
        self.data_buy['total'] = int(self.data_buy['subtotal'] + self.data_buy['fee'])
        temp = req.post(self.buy_item_url_without_listingid+listing, data=self.data_buy, headers=self.headers_buy)
        log.writetobuys(self.data_buy['subtotal'], self.data_buy['fee'],self.data_buy,listing,nome,temp.status_code,temp.content)
        temp_tuple.append(temp.status_code)
        temp_tuple.append(ast.literal_eval(temp.content))
        return temp_tuple

