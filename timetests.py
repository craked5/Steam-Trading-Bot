__author__ = 'nunosilva'

import requests as req
import timeit
import ast
import ujson
import time

def test_recent():
    steam_response = req.get('http://steamcommunity.com/market/recent/?country=PT&language=english&currency=3')
    print steam_response.status_code

def test_priceoverview():
    steam_response = req.get('http://steamcommunity.com/market/recent/?country=PT&language=english&currency=3')
    print steam_response.status_code

def test_no1inv():
    temp_inv = req.get('http://steamcommunity.com/id/craked5/inventory/json/730/2/')
    print temp_inv.status_code

def test_renderitem():
    i = 0

    req.get('http://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Urban%20DDPAT%20(Field-Tested)/render/?currency=3&start=0')
    time.sleep(0.400)

t = timeit.Timer(test_renderitem)
i = 0
while i < 100:
    print t.timeit(1)
    i += 1