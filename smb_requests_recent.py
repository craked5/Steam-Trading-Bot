#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import urllib2 as url
import requests as req
import json
import sys
import yaml
import ujson
import cookielib

my_cookies = {}



def cookies():

    pass

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
        self.host = 'http://steamcommunity.com'
        self.market = '/market'
        #currency=3 == euro
        self.item_price_viewer = '/priceoverview/?currency=3&appid=730&market_hash_name='
        self.recent_listed = '/recent/?country=PT&language=english&currency=3'
        self.complete_url_item = self.host+self.market+self.item_price_viewer
        self.complete_url_recent = self.host+self.market+self.recent_listed
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            "Host": "steamcommunity.com",
            "Cookie": "",
            "Referer": "https://steamcommunity.com/id/craked5/inventory",
            "Origin": "https://steamcommunity.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.data_sell = {
            "sessionid" : "",
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
            'sessionid': "",
            'currency': 3,
            'subtotal': 0,
            'fee': 0,
            'total': 0
        }
        self.sell_item_url = self.host+self.market+'/sellitem/'
        self.buy_item_url_without_listingid = self.host+self.market+'/buylisting/'

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
        recent_temp = ujson.loads(steam_response.text)
        #recent_temp = decode_dict(recent_temp)
        return recent_temp

    def sellitem(self,assetid,price):
        self.data_sell['assetid'] = assetid
        self.data_sell['price'] = price
        return req.post(self.sell_item_url, data=self.data_sell, headers=self.headers)

    def buyitem(self):
        pass