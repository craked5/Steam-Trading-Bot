#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

from smb_requests_recent import SteamBotHttp
from smb_logic import Logic
from smb_json_recent import SteamJsonRecent
import time
import sys
import os
import signal

print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
print 'What time interval do you want the queries to be? (number only please)\n'
http_interval = raw_input()
http_interval = float(http_interval)
print '\n'
print "OK now time one of the following commands: start, showlist, add, delete, login\n"
log = Logic()
http = SteamBotHttp()
js = SteamJsonRecent()
fork_list = []
commands = ['start','add','login','showlist','delete','quit']

def startbuying():
    i = 0
    times = []
    while True:
        try:
            start = time.clock()
            recent = {}
            recent = http.urlQueryRecent()
            js.getRecentTotalReady(recent)
            js.getfinalrecentlist()
            js.seeifbuyinggood()
            i += 1
            print i
            time.sleep(http_interval)
            elapsed = time.clock()
            elapsed = elapsed - start
            print elapsed
            times.append(elapsed)
        except KeyboardInterrupt:
            print '\n'
            print "User stopped searching"
            break

try:
    while True:
        temp = raw_input()
        temp = temp.split(' ')
        if temp[0] == 'start':
            print "CTRL+C to stop!!!!!"
            newpid = os.fork()
            fork_list.append(newpid)
            if newpid == 0:
                time.sleep(2)
                startbuying()
            else:
                pids = (os.getpid(), newpid)
                print "parent: %d, child: %d" % pids
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
        elif temp[0] == 'quit':
            print "User saiu"
            for p in fork_list:
                os.kill(p,signal.SIGKILL)
            sys.exit()
        else:
            print "Command not valid, please try again!"
except KeyboardInterrupt:
    print '\n'
    print "user saiu"