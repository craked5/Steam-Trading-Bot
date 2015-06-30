#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

from smb_requests_recent import SteamBotHttp
from smb_json_recent import SteamJsonRecent
from smb_json_item import SteamJsonItem
import time
import sys
import os
import signal

print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
print 'What time interval do you want the queries to be? (number only please)\n'
http_interval = raw_input()
http_interval = float(http_interval)
print '\n'
print "OK now time one of the following commands: startsell ,startnosell ,buy ,sell , showlist, add, delete, login\n"
http = SteamBotHttp()
js = SteamJsonRecent()
fork_list = []
commands = ['startnosell','startsell','buyinditem','howmanyprocs','showlistproc','killproc','add','login','showlist','delete','quit','sell']

#STARTBUYINGSELL NUMBER 2 NO BULLSHIT CODES
#temp_resp e a resposta do seeifbuy
#temp[0] = True
#temp[1] = assetid
#temp[2] = price
def startbuyingsell():
    i = 0
    times = []
    while True:
        start = time.time()
        recent = http.urlQueryRecent()
        if recent == False:
            print "CONN REFUSED, sleeping..."
            time.sleep(30)
            pass
        elif type(recent) == dict:
            js.getRecentTotalReady(recent)
            js.getfinalrecentlist()
            resp = js.seeifbuyinggood()
            print resp
            if resp[0] is True:
                print "OK SELLING ITEM"
                temp_one = http.getpositiononeiteminv()
                sell_response = http.sellitem(temp_one,resp[1])
                js.writetosellfile(sell_response[0],sell_response[1],resp[2],resp[1])
                js.writetowalletadd(resp[1])
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

def startbuyinditem(list_items,proc_name):
    jsind = SteamJsonItem(list_items)
    while True:
        start = time.time()
        item = http.urlQueryRecent()
        if item == False:
            print "CONN REFUSED, sleeping..."
            time.sleep(30)
            pass
        elif type(item) == dict:
            jsind.getitemtotalready(item)
            jsind.getfinalitemlist()
            temp_resp = jsind.seeifbuyinggood()
            print temp_resp[0]
            if temp_resp[0] is True:
                print "OK SELLING ITEM"
                temp_one = http.getpositiononeiteminv()
                sell_response = http.sellitem(temp_one,temp_resp[1])
                jsind.writetosellfile(sell_response[0],sell_response[1],temp_resp[2],temp_resp[1])
                js.writetowalletadd(temp_resp[1])
            time.sleep(http_interval)
            elapsed = time.time()
            elapsed = elapsed - start
            #print 'O TEMPO DO '+ proc_name + ' FOI DE ' + str(elapsed)
        else:
            time.sleep(http_interval)
            elapsed = time.time()
            elapsed = elapsed - start
            #print 'O TEMPO DO '+ proc_name + ' FOI DE ' + str(elapsed)


try:
    process_items = {}
    while True:
        try:
            temp = raw_input()
            temp = temp.split(' ')

            if temp[0] == 'login':
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
                http.login()

            elif temp[0] == 'sell':
                js.sellitemtest(temp[1], float(temp[2]))

            elif temp[0] == 'balance':
                print js.getwalletbalance()

            elif temp[0] == 'buy':
                js.buyitemtest(temp[1],temp[2],int(temp[3]),int(temp[4]),int(temp[5]))

            elif temp[0] == 'showlistproc':
                for n_proc in process_items:
                    print n_proc + '\n'
                    print str(process_items[n_proc]) + '\n'
                    print fork_list

            elif temp[0] == 'killproc':
                proctokill = raw_input('Insira o nome do processo para matar (faca showlistproc se nao souber): ')
                for proc in process_items.keys():
                    if proc == proctokill:
                        os.kill(int(process_items[proc]),signal.SIGKILL)
                        fork_list.pop(process_items[proc])
                        process_items[proc].pop()
                        print "MATOU O PROCESSO PARA COMPRAR e VENDER O ITEM " + proc
                        break

            elif temp[0] == 'howmanyprocs':
                print 'EXISTEM ' + str(len(process_items.keys())) + ' PROCESSOS A FUNCIONAR\n'

            elif temp[0] == 'buyinditem':
                temp_items = raw_input("Insira o item e as suas vertentes que quer comprar (separados por ,): \n")
                temp_items = temp_items.split(',')
                print temp_items
                process_items[temp[1]] = os.fork()
                fork_list.append(process_items[temp[1]])
                print process_items
                if process_items[temp[1]] == 0:
                    time.sleep(2)
                    startbuyinditem(temp_items,temp[1])
                else:
                    pids = (os.getpid(), process_items[temp[1]])
                    print "parent: %d, child: %d" % pids

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

