#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import urllib2 as url
import requests as req
import json
import sys
import yaml
import ujson

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

    def __init__(self, time):
        self.interval = time
        self.host = 'http://steamcommunity.com'
        self.market = '/market'
        #currency=3 == euro
        self.item_price_viewer = '/priceoverview/?currency=3&appid=730&market_hash_name='
        self.recent_listed = '/recent/?country=PT&language=english&currency=3'
        self.complete_url_item = self.host+self.market+self.item_price_viewer
        self.complete_url_recent = self.host+self.market+self.recent_listed

    def urlQueryItem(self,item):
        steam_response = req.get(self.complete_url_item + item)
        item_temp = ujson.loads(steam_response.text)
        item_temp = decode_dict(item_temp)
        return item_temp

    def urlQueryRecent(self):
        steam_response = req.get(self.complete_url_recent)
        recent_temp = ujson.loads(steam_response.text)
        #recent_temp = decode_dict(recent_temp)
        return recent_temp
