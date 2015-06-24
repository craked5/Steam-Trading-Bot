#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

from smb_requests_recent import SteamBotHttp
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
print "OK now time one of the following commands: startsel,startnosell,buy,sell, showlist, add, delete, login\n"
http = SteamBotHttp()
js = SteamJsonRecent()
fork_list = []
commands = ['startnosell','startsell','add','login','showlist','delete','quit','sell']

def startbuyingnosell():
    i = 0
    times = []
    while True:
        try:
            start = time.clock()
            recent = {}
            recent = http.urlQueryRecent()
            if recent == False:
                print "CONN REFUSED, sleeping..."
                time.sleep(30)
                pass
            elif recent == -1:
                print "LISTAS RECENTS IGUAIS, TENTANDO DE NOVO!!!!!!"
                pass
            try:
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
            except AttributeError:
                print "error, a continuar"
        except KeyboardInterrupt:
            print '\n'
            print "User stopped searching"
            break

#temp_resp e a resposta do seeifbuy
#temp[0] = True
#temp[1] = assetid
#temp[2] = price
def startbuyingsell():
    i = 0
    times = []
    while True:
        try:
            start = time.time()
            recent = http.urlQueryRecent()
            if recent == False:
                print "CONN REFUSED, sleeping..."
                time.sleep(30)
                pass
            elif recent == -1:
                time.sleep(0.200)
                print "recent igual, trying again"
            elif type(recent) == dict:
                js.getRecentTotalReady(recent)
                js.getfinalrecentlist()
                temp_resp = js.seeifbuyinggood()
                print temp_resp[0]
                if temp_resp[0] is True:
                    print "OK SELLING ITEM"
                    sell_response = http.sellitem(temp_resp[1],temp_resp[2])
                    js.writetosellfile(sell_response[0],sell_response[1],temp_resp[3],temp_resp[2])
                i += 1
                print i
                time.sleep(http_interval)
                elapsed = time.time()
                elapsed = elapsed - start
                print elapsed
            else:
                time.sleep(http_interval)
                i += 1
                print i
                elapsed = time.time()
                elapsed = elapsed - start
                print elapsed
        except KeyboardInterrupt:
            print '\n'
            print "User stopped searching"
            break


try:
    while True:
        try:
            temp = raw_input()
            temp = temp.split(' ')
            if temp[0] == 'startnosell':
                print "STARTING ONLY BUYING MODE"
                print "CTRL+C to stop!!!!!"
                newpid = os.fork()
                fork_list.append(newpid)
                if newpid == 0:
                    time.sleep(2)
                    startbuyingnosell()
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids
            elif temp[0] == 'login':
                http.login()
            elif temp[0] == 'startsell':
                print "STARTING BUYING AND SELLING MODE"
                print "CTRL+C to stop!!!!!"
                newpid = os.fork()
                fork_list.append(newpid)
                if newpid == 0:
                    time.sleep(2)
                    startbuyingsell()
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids
            elif temp[0] == 'showlist':
                print 'This is the item list: '
                print js.getlistbuyitems()
            elif temp[0] == 'delete':
                item_rem = raw_input('Item to remove from the list: ')
                js.delInItemsTxt(item_rem)
            elif temp[0] == 'add':
                item_add = raw_input('Item to add to the list: ')
                js.writeInItemsTxt(item_add)
            elif temp[0] == 'login':
                pass
            elif temp[0] == 'sell':
                http.sellitem(temp[1], float(temp[2]))
            elif temp[0] == 'buy':
                http.buyitem(temp[1],int(temp[2]),int(temp[3]),int(temp[4]))
            elif temp[0] == 'quit':
                print "User saiu"
                for p in fork_list:
                    os.kill(p,signal.SIGKILL)
                sys.exit()
            else:
                print "Command not valid, please try again!"
        except KeyboardInterrupt:
            print '\n'
            print "User saiu"
            for p in fork_list:
                os.kill(p,signal.SIGKILL)
                sys.exit()
except KeyboardInterrupt:
    print '\n'
    print "user saiu"

