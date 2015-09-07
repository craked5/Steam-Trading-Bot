#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva, github.com/craked5'

from json_item import SteamJsonItem
from json_recent_thread import SteamJsonRecentThreading
import ujson
import time
import sys
import os
import signal
import random

print 'HELLO DEAR FRIEND, THANK YOU FOR TRYING THIS SHITTY BOT EHEH NOW LETS BEGIN ASKING THE bIG QUESTIONS :D \n'
print 'IF YOU NEED TO SEE THE COMMANDS AVAILABLE TYPE commands\n'

http_interval = raw_input('What time interval do you want the queries to be on RECENT? (number only please) \n')
http_interval = float(http_interval)
http_interval_item = raw_input('And on the Individual Item Mode: \n')
http_interval_item = float(http_interval_item)
ind_item_hosts = raw_input('Do you want to change the hosts for the Individual Item Mode? (y/n) \n')
if ind_item_hosts == 'y':
    ind_item_hosts_list = raw_input('What hosts do you want to use in ind item? (us1/us2/eu/asia/world) \n')
dif_countries = raw_input('Quer mudar os country code do modo ind item (n/y)? \n')
items_list = raw_input('What is the item list that you want to load for the Recent Listings Mode? (defaults are: '
                       'items_pobre, items_pobre50, items) \n')

list_median_prices = {}
fork_list = []
cookies_json = {}
password_json = {}
setup_cookies = False
setup_password = False


#----------------------------FUNCTIONS TO SET COOKIES AND PASSWORD TO FILE (Has to restart afet)------------------------
def setPassword():

    username = raw_input('Please type your username: \n')
    password = raw_input('Please type your password: \n')

    password_json['password'] = password
    password_json['username'] = username

    try:
        password_json_file = open('util/password.json', 'w')
        ujson.dump(password_json, password_json_file)
        password_json_file.close()
    except IOError:
        print "Error opening password.json file"
        return False
    except ValueError:
        print "Error dumping data to password.json file"
        return False

    print "Done, please restart the program or it wont work! \n"

def setCookies():
    wte = raw_input("Please input your webTradeEligibility cookie: \n")
    sessionid = raw_input("Please input your sessionid cookie: \n")
    steamLogin = raw_input("Please input your steamLogin cookie: \n")
    steamLoginSecure = raw_input("Please input your steamLoginSecure cookie: \n")
    sma = raw_input("Please input your steamMachineAuth cookie (name+value together): \n")
    steamRememberLogin = raw_input("Please input your steamRememberLogin cookie: \n")

    cookies_json['webTradeEligibility'] = wte
    cookies_json['sessionid'] = sessionid
    cookies_json['steamLogin'] = steamLogin
    cookies_json['steamLoginSecure'] = steamLoginSecure
    cookies_json['steamMachineAuth'] = sma
    cookies_json['steamRememberLogin'] = steamRememberLogin

    try:
        cookies_json_file = open('util/cookies.json', 'w')
        ujson.dump(cookies_json, cookies_json_file)
        cookies_json_file.close()
    except IOError:
        print "Error opening cookie.json file"
        return False
    except ValueError:
        print "Error dumping data to cookie.json file"
        return False
#-----------------------------------------------------------------------------------------------------------------------
#------------------------------------INITIALIZE AN INSTANCE OF THE RECENT LISTINGS MODE---------------------------------
try:
    cookies_json_file = open('util/cookies.json', 'r')
    cookies_json = ujson.load(cookies_json_file)

    wte = cookies_json.get('webTradeEligibility').encode('ascii','ignore')
    sma = cookies_json.get('steamMachineAuth').encode('ascii','ignore')
    sessionid = cookies_json.get('sessionid').encode('ascii','ignore')
    slc = cookies_json.get('steamLoginSecure').encode('ascii','ignore')
    sl = cookies_json.get('steamLogin').encode('ascii','ignore')
    srl= cookies_json.get('steamRememberLogin').encode('ascii','ignore')
    setup_cookies = True
except IOError:
    print 'NO COOKIES AND PASSWORD DETECTED \n'
    print 'PLEASE PLEASE SET YOUR COOKIES BEFORE DOING ANYTHING, YOU CAN DO THAT BY ' \
          'TYPING setcookies \n'
except ValueError:
    print 'NO COOKIES AND PASSWORD DETECTED \n'
    print 'PLEASE PLEASE SET YOUR COOKIES BEFORE DOING ANYTHING, YOU CAN DO THAT BY ' \
          'TYPING setcookies \n'

try:
    password_json_file = open('util/password.json', 'r')
    password_json = ujson.load(password_json_file)
    password = password_json.get('password').encode('ascii','ignore')
    username = password_json.get('username').encode('ascii','ignore')
    setup_password = True
except IOError:
    print "PASSWORD NOT DETECTED, PLEASE TYPE setpassword TO SET YOUR PASSWORD"
except ValueError:
    print "error opening the password.json file, please try to set your password manually by tying setpassword"

if setup_password and setup_cookies:
    print "YOU ARE LOGGED WITH THE USERNAME: " + username
    jst = SteamJsonRecentThreading(items_list,wte,sma,sessionid,slc,sl,srl,password,username)
else:
    print "Error regarding the cookies or the password, maybe they haven't been setup"
    print "Do you want to set them up now? (y/n) \n"
    if raw_input() == 'y':
        setCookies()
        setPassword()
    else:
        print "Please check your cookies and password file, maybe it's path is wrong"
        sys.exit()
#-----------------------------------------------------------------------------------------------------------------------

def startbuyinditem(item_buy, proc_name):
    jsind = SteamJsonItem(item_buy, ind_item_hosts_list, dif_countries,wte,sma,sessionid,slc,sl,srl,password,username)
    i = 0
    sleep_time_down = 165
    while True:
        # start = time.time()
        item_json = jsind.urlqueryspecificitemind(item_buy)
        if item_json == False:
            jsind.setdownstate(1)
            if jsind.getdownstate() == 1:
                sleep_time_down += 15
                print "CONN REFUSED" + ' on item_json ' + item_buy + ' at try ' + str(i) + ', sleeping for ' + \
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

                if ((float(lowest_price) + (0.02 * float(lowest_price))) / float(resp[3])) >= 1.07:
                    price_sell = float(lowest_price)
                    price_sell_str = "{0:.2f}".format(price_sell)
                    print price_sell
                else:
                    price_sell = float(resp[1] * 0.95)
                    price_sell_str = "{0:.2f}".format(price_sell)
                    print price_sell

                price_sell_without_fee = price_sell / 1.15
                print price_sell_without_fee

                sell_response = jsind.sellitem(id_item_pos_one, float(price_sell_without_fee))

                if sell_response[0] == 200:
                    jsind.writetosellfile(sell_response[0], sell_response[1], resp[2], price_sell_str, 0)

                elif sell_response[0] == 502:
                    jsind.writetosellfile(sell_response[0], sell_response[1], resp[2], price_sell_str, 0)

            i += 1
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'
            elif i % 250 == 0:
                if jsind.seeifanyitemsold():
                    jsind.parsewalletbalanceandwrite()
                print "CHEGUEI AS " + str(i) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                time.sleep(random.randint(10, 20))

            time.sleep(http_interval_item)

        else:
            i += 1
            if i % 10 == 0:
                print proc_name + ' is still kicking ass, let me work please! ty<3'

            elif i % 250 == 0:
                if jsind.seeifanyitemsold():
                    jsind.parsewalletbalanceandwrite()
                print "CHEGUEI AS " + str(i) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                time.sleep(random.randint(10, 20))

            time.sleep(http_interval_item)


try:
    process_items = {}
    while True:
        try:
            command_input = raw_input('Insira o comando que pretende usar: ')
            command_input = command_input.split(' ')

            if command_input[0] == 'login':
                jst.http.login()

            elif command_input[0] == 'logout':
                jst.http.logout()

            elif command_input[0] == 'commands':
                print '\n'
                print 'setcookies - sets your cookies to begin using all this shit \n'
                print 'setpassword - sets your password\n'
                print 'login - logs the user on Steam (please set your cookies and password fisrt) \n'
                print 'logout - logs the user out of Steam \n'
                print 'getmedianprices - gets the median price (defined by Steam) for the items on the users lists' \
                      '(please login first) \n'
                print 'loadmedianprices - loads the median prices from a json file (use this if you just used the ' \
                      'getmedianprices and you dont want to get them all again) \n'
                print 'dump - dumps the median price list on a json file for disk storage \n'
                print 'srt - means StartRecentThreads, starts the recent listings mode of the bot \n'
                print 'bii - starts an individual item process that checks that item page (you can start multiple ' \
                      'processes) \n'
                print 'del - deletes an item from the list of items chosen by the user \n'
                print 'searchkenny = When using the recent mode it also searches for kennys specific cobble cases! \n'
                print 'add - adds an item to the list of items chosen by the user \n'
                print 'showlist - prints the list of items chosen by the user \n'
                print 'getbalance - gets the balance from your steam wallet (please login first) \n'
                print 'seeactivelistings - gets your active sell listings \n'
                print 'procs - prints the list of names of the procs of the individual mode active \n'
                print 'howmanyprocs - prints how many individual item mode processes are active \n'
                print 'killproc - kills and individual item mode process by the name (if you dont know the name type' \
                      'procs) \n'
                print 'quit - quits the program (you can also ctrl-c to quit a process) \n'

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
                jst.exportJsonToFile(jst.list_median_prices,'median_prices')

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
                    jst.executethreads(n_threads, http_interval)
                else:
                    pids = (os.getpid(), newpid)
                    print "parent: %d, child: %d" % pids

            elif command_input[0] == 'showlist':
                print 'This is the item list: '
                print jst.getlistbuyitems()

            elif command_input[0] == 'del':
                item_rem = raw_input('Item to remove from the list: ')
                jst.delInItemsTxt(item_rem)

            elif command_input[0] == 'add':
                item_add = raw_input('Item to add to the list: ')
                jst.writeInItemsTxt(item_add)

            elif command_input[0] == 'searchkenny':
                if raw_input('Do you want to search for KennyS cobblestone cases? (y/n)') == 'y':
                    jst.search_for_kenny_cobble = True
                else:
                    print "You did not activate the KennyS cobble search mode!"

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

            elif command_input[0] == 'updateactivelistings':
                temp = jst.updateactivelistings()
                print temp

            elif command_input[0] == 'buy':
                jst.buyitemtest(command_input[1], int(command_input[2]), int(command_input[3]),
                                int(command_input[4]), command_input[5])

            elif command_input[0] == 'procs':
                for n_proc in process_items:
                    print n_proc + '  ' + str(process_items[n_proc])
                print fork_list

            elif command_input[0] == 'setcookies':

                if setCookies() == False:
                    print "Error setting your cookies, please restart and try again!"
                print "Done, please restart the program or it wont work! \n"

            elif command_input[0] == 'setpassword':

                if setPassword() == False:
                    print "Error setting your password, please restart and try again!"
                print "Done, please restart the program or it wont work! \n"

            elif command_input[0] == 'killproc':
                proctokill = raw_input('Insira o nome do processo para matar (faca showlistproc se nao souber): ')
                for proc in process_items.keys():
                    if proc == proctokill:
                        os.kill(int(process_items[proc]), signal.SIGKILL)
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
                    startbuyinditem(item_name, proc_name)
                else:
                    pids = (os.getpid(), process_items[proc_name])
                    print "parent: %d, child: %d" % pids

            elif command_input[0] == 'quit':
                print "User saiu"
                for p in fork_list:
                    os.kill(p, signal.SIGKILL)
                    print 'MATEI O PROCESSO ' + str(p)
                sys.exit()
            else:
                print "Command not valid, please try again!"
        except KeyboardInterrupt:
            print '\n'
            print "User saiu"
            for p in fork_list:
                os.kill(p, signal.SIGKILL)
                sys.exit()
except KeyboardInterrupt:
    print '\n'
    print "user saiu"

