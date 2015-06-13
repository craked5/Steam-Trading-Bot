#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

from smb_requests_recent import SteamBotHttp
from smb_logic import Logic
from smb_json_recent import SteamJsonRecent
import time

print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
print 'What time interval do you want the queries to be? (number only please)'
http_interval = raw_input()
http_interval = float(http_interval)
print "OK now time one of the following commands: start, showlist, add, delete, login"
log = Logic()
http = SteamBotHttp()
js = SteamJsonRecent()
commands = ['start','add','login','showlist','delete']

def startbuying():
    i = 0
    times = []
    while i is not 200:
        start = time.clock()
        recent = {}
        recent = http.urlQueryRecent()
        js.getRecentTotalReady(recent)
        js.getfinallist()
        i += 1
        print i
        time.sleep(http_interval)
        elapsed = time.clock()
        elapsed = elapsed - start
        print elapsed
        times.append(elapsed)

while True:
    temp = raw_input()
    temp = temp.split(' ')
    if temp[0] == 'start':
        startbuying()
    elif temp[0] == 'showlist':
        print 'This is the item list: '
        print log.list_items_to_buy
    elif temp[0] == 'delete':
        item_rem = raw_input('Item to remove from the list: ')
        log.delInItemsTxt(item_rem)
    elif temp[0] == 'add':
        item_add = raw_input('Item to add to the list: ')
        log.writeInItemsTxt(item_add)
    elif temp[0] == 'login':
        pass
    else:
        print "Command not valid, please try again!"
