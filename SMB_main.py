#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

from smb_requests_recent import SteamBotHttp
from smb_logic import Logic

print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
print 'What time interval do you want the queries to be? (number only please)'
http_interval = raw_input()
log = Logic()

while True:
    temp = raw_input()
    if temp is 'start':
        pass
    elif temp is 'show list':
        print 'This is the item list: ' + log.list_items
    elif temp is 'delete':
        item_rem = raw_input('Item to remove from the list: ')
        log.delInItemsTxt(item_rem)
    elif temp is 'add':
        item_add = raw_input('Item to add to the list: ')
        log.writeInItemsTxt(item_add)
