#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva, github.com/craked5'


from http import SteamBotHttp
#from json_recent import SteamJsonRecent
from json_item import SteamJsonItem
from json_recent_thread import SteamJsonRecentThreading
import time
import sys
import os
import signal
import random

list_median_prices = {}
print 'HAI WELCOME TO THIS SHITTY BOT!!!!!!!!!!!!!! :D'
http_interval = raw_input('What time interval do you want the queries to be on RECENT? (number only please)\n')
http_interval = float(http_interval)
http_interval_item = raw_input('And on an individual item: \n')
http_interval_item = float(http_interval_item)
ind_item_hosts = raw_input('Do you want to change the hosts for ind item? (y/n) \n')
if ind_item_hosts == 'y':
    ind_item_hosts_list = raw_input('What hosts do you want to use in ind item? (us1/us2/eu/asia/world) \n')
dif_countries = raw_input('Quer mudar os country code do modo ind item (n/y)? \n')
print '\n'
print "OK now time one of the following commands: srt ,buy ,sell , showlist, add, delete, login\n"
http = SteamBotHttp()
jst = SteamJsonRecentThreading()
fork_list = []
commands = ['bii','howmanyprocs','showlistprocs','killproc','add','login',
            'showlist','delete','quit','sell','loadmedianprices','getmedianprices']

'''
#STARTBUYINGSELL NUMBER 2 NO BULLSHIT CODES
#temp_resp e a resposta do seeifbuy
#temp[0] = True
#temp[1] = assetid
#temp[2] = price
'''

def startbuyinditem(item_buy,proc_name):
    jsind = SteamJsonItem(item_buy,ind_item_hosts_list,dif_countries)
    i = 0
    sleep_time_down = 165
    while True:
        #start = time.time()
        item_json = jsind.urlqueryspecificitemind(item_buy)
        if item_json == False:
            jsind.setdownstate(1)
            if jsind.getdownstate() == 1:
                sleep_time_down += 15
                print "CONN REFUSED" + ' on item_json ' + item_buy + ' at try ' + str(i)+ ', sleeping for ' + \
                      str(sleep_time_down)
                time.sleep(sleep_time_down)
            pass
        elif type(item_json) == dict:

            jsind.setdownstate(0)
            sleep_time_down = 165

            jsind.getitemtotalready(item_json)

            jsind.getfinalitem()

            resp = jsind.buyingroutinesingleitem(list_median_prices[item_buy])
            if resp[0] is True:

                id_item_pos_one = jsind.getpositiononeiteminv()

                lowest_price = jsind.getlowestprice(resp[2])

                if ((float(lowest_price)+(0.02*float(lowest_price)))/float(resp[3])) >= 1.07:
                    price_sell = float(lowest_price)
                    price_sell_str = "{0:.2f}".format(price_sell)
                    print price_sell
                else:
                    price_sell = float(resp[1] * 0.95)
                    price_sell_str = "{0:.2f}".format(price_sell)
                    print price_sell

                price_sell_without_fee = price_sell/1.15
                print price_sell_without_fee

                sell_response = jsind.sellitem(id_item_pos_one,float(price_sell_without_fee))

                if sell_response[0] == 200:
                    jsind.writetosellfile(sell_response[0],sell_response[1],resp[2],price_sell_str,0)

                elif sell_response[0] == 502:
                    jsind.writetosellfile(sell_response[0],sell_response[1],resp[2],price_sell_str,0)

            i += 1
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'
            elif i % 250 == 0:
                if jsind.seeifanyitemsold():
                    jsind.parsewalletbalanceandwrite()
                print "CHEGUEI AS " + str(i) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                time.sleep(random.randint(10,20))

            time.sleep(http_interval_item)

        else:
            i += 1
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'

            elif i % 250 == 0:
                if jsind.seeifanyitemsold():
                    jsind.parsewalletbalanceandwrite()
                print "CHEGUEI AS " + str(i) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                time.sleep(random.randint(10,20))

            time.sleep(http_interval_item)


try:
    process_items = {}
    while True:
        try:
            command_input = raw_input('Insira o comando que pretende usar: ')
            command_input = command_input.split(' ')

            if command_input[0] == 'login':
                http.login()

            elif command_input[0] == 'logout':
                http.logout()

            elif command_input[0] == 'stuffnow':
                list_median_prices50 = {}
                for key in list_median_prices:
                    if list_median_prices[key] > 0.45:
                        list_median_prices50[key] = list_median_prices[key]
                print list_median_prices50

            elif command_input[0] == 'getmedianprices':
                list_median_prices = jst.getmedianitemlist()
                print list_median_prices

            elif command_input[0] == 'loadmedianprices':
                list_median_prices = jst.loadmedianpricesfromfile()
                print list_median_prices

            elif command_input[0] == 'dump':
                jst.exportJsonToFile(jst.list_median_prices)


            #elif command_input[0] == 'sr':
                #print "STARTING BUYING AND SELLING MODE"
                #print "CTRL+C to stop!!!!!"
                #newpid = os.fork()
                #fork_list.append(newpid)
                #if newpid == 0:
                    #time.sleep(2)
                    #jst.startbuyingsell(http_interval)
                #else:
                    #pids = (os.getpid(), newpid)
                    #print "parent: %d, child: %d" % pids

            elif command_input[0] == 'newsessionidtest':
                jst.http.httputil.sessionid = raw_input('Enter the new session id: \n')

            elif command_input[0] == 'srt':
                n_threads = raw_input('How many threads do you wish to run? \n')
                temp_balance = jst.parsewalletbalance()
                if temp_balance != False:
                    if jst.log.wallet_balance != temp_balance:
                        if type(jst.parsewalletbalanceandwrite()) == float:
                            print "Balance foi updated!"
                jst.updateactivelistings()
                newpid = os.fork()
                fork_list.append(newpid)
                if newpid == 0:
                    time.sleep(2)
                    print "STARTING BUYING ON RECENT WITH " + str(n_threads) + " THREADS MODE"
                    print "CTRL+C to stop!!!!!"
                    jst.executethreads(n_threads,http_interval)
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids

            elif command_input[0] == 'showlist':
                print 'This is the item list: '
                print jst.getlistbuyitems()

            elif command_input[0] == 'delete':
                item_rem = raw_input('Item to remove from the list: ')
                jst.delInItemsTxt(item_rem)

            elif command_input[0] == 'add':
                item_add = raw_input('Item to add to the list: ')
                jst.writeInItemsTxt(item_add)

            elif command_input[0] == 'sell':
                jst.sellitemtest(command_input[1], float(command_input[2]))

            elif command_input[0] == 'getbalance':
                ba = jst.parsewalletbalanceandwrite()
                print "O NOVO BALANCE E " + str(ba)

            elif command_input[0] == 'recenttc':
                i = 0
                for i in range(100):
                    jst.queryrecentdifhostsdifcountries(0)
                    time.sleep(0.100)

            elif command_input[0] == 'seeactivelistings':
                temp = jst.getactivelistingsparsed()
                print temp

            elif command_input[0] == 'newlisttest':
                list_median_prices50

            elif command_input[0] == 'updateactivelistings':
                temp = jst.updateactivelistings()
                print temp

            elif command_input[0] == 'buy':
                jst.buyitemtest(command_input[1],int(command_input[2]),int(command_input[3]),
                               int(command_input[4]),command_input[5])

            elif command_input[0] == 'procs':
                for n_proc in process_items:
                    print n_proc + '  ' + str(process_items[n_proc])
                print fork_list

            elif command_input[0] == 'killproc':
                proctokill = raw_input('Insira o nome do processo para matar (faca showlistproc se nao souber): ')
                for proc in process_items.keys():
                    if proc == proctokill:
                        os.kill(int(process_items[proc]),signal.SIGKILL)
                        fork_list.remove(process_items[proc])
                        process_items.pop(proc)
                        print "MATOU O PROCESSO PARA COMPRAR e VENDER O ITEM " + proc
                        break

            elif command_input[0] == 'howmanyprocs':
                print 'EXISTEM ' + str(len(process_items.keys())) + ' PROCESSOS A FUNCIONAR\n'

            elif command_input[0] == 'bii':
                proc_name = raw_input("Insira o nome do processo (normalmente algo relacionado com a arma: \n")
                item_name = raw_input('Insira o nome da arma a comprar: \n')
                temp_balance = jst.parsewalletbalance()
                if temp_balance != False:
                    if jst.log.wallet_balance != temp_balance:
                        if type(jst.parsewalletbalanceandwrite()) == float:
                            print "Balance foi updated!"
                jst.updateactivelistings()
                process_items[proc_name] = os.fork()
                fork_list.append(process_items[proc_name])
                print process_items
                if process_items[proc_name] == 0:
                    time.sleep(2)
                    startbuyinditem(item_name,proc_name)
                else:
                    pids = (os.getpid(), process_items[proc_name])
                    print "parent: %d, child: %d" % pids

            elif command_input[0] == 'quit':
                print "User saiu"
                for p in fork_list:
                    os.kill(p,signal.SIGKILL)
                    print 'MATEI O PROCESSO ' + str(p)
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

