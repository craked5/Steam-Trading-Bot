#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva, github.com/craked5'

import time
import threading
import ujson
import decimal
import random
import unicodedata
from bs4 import BeautifulSoup
from logic import Logic
from http import SteamBotHttp


class SteamJsonRecentThreading:

    def __init__(self,items_list,wte,sma,sessionid,sls,sl,srl,password,username):
        self.recent_parsing_list = [u'results_html',u'hovers',u'last_listing',u'last_time',u'app_data',u'currency',
                                    u'success',u'more',u'purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount',
                                   'status','original_amount','tradable',
                                   'background_color','icon_url','icon_url_large',
                                   'descriptions','name','name_color','type',
                                   'market_name','market_actions','commodity','app_icon',
                                   'owner','actions','market_tradable_restriction']
        self.listinginfo_parsing_list = ['fee','publisher_fee_percent','steam_fee','publisher_fee',
                                         'converted_steam_fee','converted_publisher_fee','converted_price_per_unit',
                                         'converted_fee_per_unit','converted_fee_per_unit',
                                         'converted_publisher_fee_per_unit','price',
                                         'publisher_fee_app','converted_steam_fee_per_unit']
        self.listinginfo_asset_parsing_list = ['currency','contextid','amount','market_actions','appid']
        self.float100 = float(100)
        self.http = SteamBotHttp(wte,sma,sessionid,sls,sl,srl,password,username)
        #logic mode recent
        #logic mode item
        self.log = Logic('recent',0,0,items_list)
        self.last_listing_buy = ''
        self.dif_countries = self.log.dif_countries
        self.dif_hosts = self.log.dif_hosts_recent
        self.contaSim = 0
        self.contaNao = 0
        self.list_median_prices = {}
        self.timestamp_lock = threading.Lock()
        self.buy_lock = threading.Lock()
        self.sell_lock = threading.Lock()
        self.last_listing_buy_lock = threading.Lock()
        self.write_active_listings_lock = threading.Lock()
        self.timestamp = ''
        self.search_for_kenny_cobble = False

    def getRecentTotalReady(self, recent_full):
        self.recent_parsed = {}

        if self.search_for_kenny_cobble is True:
            self.searchkenny(recent_full)

        if type(recent_full) == dict:
            for key in self.recent_parsing_list:
                if recent_full.has_key(key):
                    recent_full.pop(key)
        else:
            recent_full = {}
        #retorna um dict so com as keys assets e listinginfo
        return recent_full

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ASSETS!!!!!!!!!!!!!!----------------------------------------------------

    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getCleanAssetList(self,recent_parsed):
        if recent_parsed.has_key('assets'):
            asset_list = recent_parsed['assets']
            if asset_list.has_key('730'):
                asset_list = asset_list['730']
                asset_list = asset_list['2']
                for key_item in asset_list:
                    for key in self.asset_parsing_list:
                        if key in asset_list[key_item]:
                            asset_list[key_item].pop(key)
            else:
                return False
        else:
            return False
        return asset_list

    #lista final dos assets = list2 = {'awp worm god':'231342342','ak47 redline':'432342342342',...}
    #nao executar, so no getfinallist()
    def getlistassets(self,asset_list):
        if asset_list == False:
            return False
        else:
            final_list_assets = {}
            for key_item in asset_list.keys():
                if asset_list[key_item].has_key('market_hash_name'):
                    final_list_assets[asset_list[key_item]['market_hash_name']] \
                    = asset_list[key_item]['id']
            return final_list_assets

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------LISTINGS!!!!!!!!!!!--------------------------------------------------------

    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    #1 a ser executada
    def delNonCsgoListings(self, recent_parsed):
        listinginfo_list = {}
        if recent_parsed.has_key('listinginfo'):
            temp_list = recent_parsed['listinginfo']
            listinginfo_list = temp_list
            for k in listinginfo_list.keys():
                if listinginfo_list[k]['asset']['appid'] != 730:
                    listinginfo_list.pop(k)
                elif listinginfo_list[k]['asset']['amount'] == 0:
                    listinginfo_list.pop(k)
        else:
            return False
        return listinginfo_list

    #2 a ser executada
    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getCleanListinginfoListWithAsset(self,listinginfo_list):
        temp_dict = listinginfo_list
        if temp_dict == False:
            return False
        else:
            for key_item in temp_dict:
                for key in self.listinginfo_parsing_list:
                    if temp_dict[key_item].has_key(key):
                        temp_dict[key_item].pop(key)
        return temp_dict

    #3 a ser executada
    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getcleanlistings(self,listinginfo_list):
        temp_dict = listinginfo_list
        if temp_dict == False:
            return False
        else:
            for key_item in temp_dict:
                for key in self.listinginfo_asset_parsing_list:
                    if temp_dict[key_item]['asset'].has_key(key):
                        temp_dict[key_item]['asset'].pop(key)
        return temp_dict

    #lista final dos listings: list1 = {'231342342':'2.45','432342342342':'12.76',...
    #nao executar, so no getfinallist()
    def getlistlistings(self,listinginfo_list):

        final_list_listings = listinginfo_list

        if final_list_listings != False:
            for key_item in final_list_listings.keys():
                if final_list_listings[key_item].has_key('converted_price') == False:
                    final_list_listings.pop(key_item)
        else:
            return False

        return final_list_listings
        #except:
            #print "falha no parsing da lista de listings"
            #return False

#-------------------------------------------------------------------------------------------------------------------

    def getfinalrecentlist(self,asset_clean,listing_clean):
        final_list = {}

        if type(listing_clean) == dict:
            listing_clean_this = listing_clean
        else:
            print 'falha no parsing dos listings, try again'
            return False

        if type(asset_clean) == dict:
            asset_clean_this = asset_clean
        else:
            print 'falha no parsing dos assets, try again'
            return False

        for k in listing_clean_this:
            for k2 in asset_clean_this:
                if asset_clean_this.get(k2) == listing_clean_this[k]['asset']['id']:
                    final_list[k2] = listing_clean_this.get(k)
        return final_list

    def seeifrecentiteminlistbuy(self,item):
        for temp in self.log.list_items_to_buy:
            if item == temp:
                return True

    #This function analizes if an item found on a RECENT_LISTING response from Steam belongs in the item list that the
    #user defined and if so it analizes if its worth buying
    #
    #Returns False if anything goes wrong
    def buyingroutine(self,final_list,t_name,host):
        temp_resp = []
        if final_list == False:
            temp_resp.append(False)
            return temp_resp
        else:
            final_list_this = final_list
            for key in final_list_this:
                if key in self.log.list_items_to_buy_unicode:
                    if self.list_median_prices.has_key(key):
                        temp_converted_price_math = float(decimal.Decimal(final_list_this[key]['converted_price'])/100)
                        temp_converted_fee_math = float(decimal.Decimal(final_list_this[key]['converted_fee'])/100)
                        if float(float(self.list_median_prices[key]) -
                                float((temp_converted_price_math+temp_converted_fee_math))) >= \
                                (0.275*(float(self.list_median_prices[key]))):
                            if (temp_converted_price_math+temp_converted_fee_math) <= \
                                    float((95*self.getwalletbalancefromvar())):
                                if int(final_list_this[key]['converted_currencyid']) == 2003:
                                    if final_list_this[key]['listingid'] != self.last_listing_buy:

                                        self.last_listing_buy_lock.acquire()
                                        self.last_listing_buy = final_list_this[key]['listingid']
                                        self.last_listing_buy_lock.release()

                                        print 'Estou prestes a entrar no acquire dos buys ON THREAD ' + str(t_name)
                                        self.buy_lock.acquire()
                                        print 'Entrei no acquire dos buys ON THREAD '  + str(t_name)

                                        try:
                                            if (float(self.list_median_prices[key]) - float(self.getlowestprice(key))) \
                                                    >= (0.15*float(self.list_median_prices[key])):
                                                print "O PRECO LOWEST E MT MAIS BAIXO QUE O MEDIO, NAO VOU COMPRAR"
                                                print 'sai do lock dos buys ON THREAD ' + str(t_name)
                                                self.buy_lock.release()
                                                temp_resp.append(False)
                                                return temp_resp
                                        except (TypeError,KeyError):
                                            self.buy_lock.release()
                                            temp_resp.append(False)
                                            return temp_resp

                                        temp = self.http.buyitem(final_list_this[key]['listingid'],
                                                                 final_list_this[key]['converted_price'],
                                                                 final_list_this[key]['converted_fee'],
                                                                 final_list_this[key]['converted_currencyid'],host)

                                        self.log.writetobuyfile(self.http.httputil.data_buy['subtotal'],
                                                                self.http.httputil.data_buy['fee'],
                                                                self.http.httputil.data_buy,
                                                                final_list_this[key]['listingid'],
                                                                key,temp[0],temp[1],t_name)

                                        if temp[0] == 200:
                                            if temp[1]['wallet_info'].has_key('wallet_balance'):
                                                if self.log.writetowallet(temp[1]['wallet_info']['wallet_balance']) == True:
                                                    print "Ok COMPREI A: " + key + " ao preco: " + \
                                                         str(final_list_this[key]['converted_price'] +
                                                             final_list_this[key]['converted_fee'])
                                                    temp_resp.append(True)
                                                    temp_resp.append(self.list_median_prices[key])
                                                    temp_resp.append(key)
                                                    temp_resp.append(temp_converted_fee_math+temp_converted_price_math)
                                                    self.buy_lock.release()
                                                    print 'sai do lock dos buys ON THREAD ' + str(t_name)
                                                    return temp_resp
                                        else:
                                            print "Nao pude comprar item " + key
                                            print "erro ao comprar item"
                                            self.buy_lock.release()
                                            print 'sai do lock dos buys ON THREAD ' + str(t_name)
                                            temp_resp.append(False)
                                            return temp_resp
                                    else:
                                        temp_resp.append(False)
                                        return temp_resp
                            else:
                                print "Nao pude comprar: " + key +" porque nao tenho fundos On THREAD " + str(t_name)
                                temp_resp.append(False)
                                return temp_resp
                        else:
                            print "THREAD " + str(t_name) + " nao pode comprar " + key + \
                                  " porque margens nao sao suficientes. " \
                                  "Preco medio: " + str(self.list_median_prices[key]) +\
                                  ' Preco do item: ' + str(temp_converted_fee_math+temp_converted_price_math)
                            temp_resp.append(False)
                            return temp_resp
                    else:
                        temp_resp.append(False)
                        return temp_resp
        temp_resp.append(False)
        return temp_resp

#----------------------------------------------AUX FUNCTIONS-----------------------------------------------------------
    #Calls the querie recent function on the HTTP class
    def queryrecent(self,thread):
        lista = []
        lista.append(self.http.queryrecent('steamcommunity.com',thread))
        lista.append('steamcommunity.com')
        return lista

    #Calls the querie recent function on the HTTP class with diferent country codes!
    def queryrecentdifcountries(self,thread):
        country = random.choice(self.log.list_countries)
        lista = []
        lista.append(self.http.urlqueryrecentwithcountry('steamcommunity.com',country,thread))
        lista.append('steamcommunity.com')
        return lista

    #Calls the querie recent function on the HTTP class with diferent hosts
    def queryrecentdifhosts(self,thread):
        host = random.choice(self.log.list_hosts)
        lista = []
        lista.append(self.http.queryrecent(host,thread))
        lista.append(host)
        return lista

    #Calls the querie recent function on the HTTP class with diferent hosts and country codes
    def queryrecentdifhostsdifcountries(self,thread):
        host = random.choice(self.log.list_hosts)
        country = random.choice(self.log.list_countries)
        lista = []
        lista.append(self.http.urlqueryrecentwithcountry(host,country,thread))
        lista.append(host)
        return lista

    #Returns the id of the item with the number 1 position on your inventory or False if anything goes wrong
    def getpositiononeiteminv(self):
        return self.http.getpositiononeiteminv()

    def sellitem(self,assetid,price):
        return self.http.sellitem(assetid,price)

    def exportJsonToFile(self,json,file):
        try:
            with open('util/'+file+'.json', 'w') as outfile:
                ujson.dump(json, outfile)
            outfile.close()
        except ValueError:
            return False
        return True

    def writeInItemsTxt(self,item):
        return self.log.writeInItemsTxt(item)

    def delInItemsTxt(self,item):
        return self.log.delInItemsTxt(item)

    def getlistbuyitems(self):
        return self.log.list_items_to_buy

    #Returns the balance from the VAR in log.wallet_balance
    def getwalletbalancefromvar(self):
        return float(self.log.wallet_balance)

    #Loads the median prices from the file median_prices.json
    #Return false in case of error
    def loadmedianpricesfromfile(self):
        try:
            file = open('util/median_prices.json','r')
            self.list_median_prices = ujson.load(file)
            file.close()
        except ValueError:
            return False

        return self.list_median_prices

    def writetosellfile(self,status,content,item,price,thread_n,price_no_fee):
        return self.log.writetosellfile(status,content,item,price,thread_n,price_no_fee)

    def writetobuyfile(self,subtotal,fee,data_buy,listingid,key,responsecode,responsedict,thread_n):
        return self.log.writetobuyfile(subtotal,fee,data_buy,listingid,key,responsecode,responsedict,thread_n)

    def sellitemtest(self,assetid,price):
        return self.http.sellitem(assetid,price)

    #Writes to the wallet file the balance that is currently stored in the var Walletbalance
    #IT DOES NOT RETURN OR WRITE THE BALANCE DIRECTLY FROM STEAM
    def writetowalletadd(self,amount_add):
        temp = float(amount_add) + float(self.getwalletbalancefromvar())
        temp = temp*100
        return self.log.writetowallet(int(temp))

    #Returns the lowest price for the item directly from Steam
    #In case of error returns False
    def getlowestprice(self,item):
        temp_item_priceover = self.http.querypriceoverview(item)
        if type(temp_item_priceover) == int:
            print "Erro ao obter preco mais baixo actualmente de " + item
            print "Status code da querie: " + str(temp_item_priceover)
            return False

        if type(temp_item_priceover) == bool:
            return False

        elif temp_item_priceover.has_key('lowest_price'):
            temp_lowest_price = temp_item_priceover['lowest_price']
            if isinstance(temp_lowest_price, basestring):
                temp_lowest_price = temp_lowest_price.replace('&#8364; ','').replace(',','.').replace('-','0')
                temp_lowest_price = "{0:.2f}".format(float(temp_lowest_price))
                print temp_lowest_price
                return temp_lowest_price

    def buyitemtest(self,listing,subtotal,fee,currency,host):
        temp =  self.http.buyitemTEST(listing,subtotal,fee,currency,host)
        print str(temp[0]) + '\n'
        print temp[1]

    #returns the median price for every item on the list that the user chooses at the start of the program
    #In case of error for any item, you will not get that item median price
    def getmedianitemlist(self):

        self.list_median_prices = {}

        for key in self.log.list_items_to_buy_unicode:
            temp_item_priceover = {}
            temp_item_priceover = self.http.querypriceoverview(key.encode('utf-8'))
            if type(temp_item_priceover) == int:
                print "Erro ao obter preco medio de " + key
                print "Status code da querie: " + str(temp_item_priceover)

            elif type(temp_item_priceover) == bool:
                print "Erro ao obter preco medio de " + key
                print "Status code da querie: " + str(temp_item_priceover)

            elif temp_item_priceover.has_key('median_price'):
                temp_median_price = temp_item_priceover['median_price']
                if isinstance(temp_median_price, basestring):
                    temp_median_price = temp_median_price.decode('unicode_escape').encode('ascii','ignore')
                    temp_median_price = temp_median_price.replace(',','.').replace('-','0')
                    temp_median_price = "{0:.2f}".format(float(temp_median_price))
                self.list_median_prices[key] = float(temp_median_price)

            if self.list_median_prices.has_key(key):
                print 'O preco medio de ' + key + ' e: ' + str(self.list_median_prices[key])

        return self.list_median_prices

    #returns wallet balance from steam website in float format
    def parsewalletbalance(self):
        soup = BeautifulSoup(self.http.getsteamwalletsite(),'html.parser')
        balance_soup = soup.find('span',{'id':'marketWalletBalanceAmount'})

        if balance_soup != None:
            balance_soup = balance_soup.get_text()
            balance_str = balance_soup.encode('ascii','ignore').replace(',','.').replace('-','0')

            return float(balance_str)
        else:
            print "ERROR GETTING WALLET BALANCE, TRY TO LOGIN AGAIN!"
            return False


    #Vai buscar o valor o balance da minha carteira ao Steam diretamente
    #e se encontrar, atualiza a var wallet_balance
    def parsewalletbalanceandwrite(self):

        soup = BeautifulSoup(self.http.getsteamwalletsite(),'html.parser')
        balance_soup = soup.find('span',{'id':'marketWalletBalanceAmount'})

        if balance_soup != None:
            balance_soup = balance_soup.get_text()
            balance_str = balance_soup.encode('ascii','ignore').replace(',','.').replace('-','0')

            self.log.writetowallet(float(balance_str)*100)

            return float(balance_str)
        else:
            print "ERROR GETTING WALLET BALANCE, MAYBE FAZER LOGIN RESOLVE ESTE PROBLEMA"
            return False

    #faz uma querie para ver as active listings que a conta tem
    #retorna as active_listings actuais ou false
    def getactivelistingsparsed(self):
        active_listings = self.http.getmyactivelistingsraw()
        active_listings_list = []

        if type(active_listings) == dict:
            if active_listings.has_key('assets'):
                if type(active_listings['assets']) == dict:
                    if active_listings['assets'].has_key('730'):
                        active_listings = active_listings['assets']['730']['2']

                        for id in active_listings:
                            active_listings_list.append(id)

                        print type(active_listings_list)
                        return active_listings_list
                else:
                    return False
        else:
            return False

    #returns new active listings list or False
    def updateactivelistings(self):
        temp = self.getactivelistingsparsed()
        if temp != False:
            if type(self.log.writenewactivelistings(temp)) == list:
                print "NEW ACTIVE LISTINGS: \n"
                return self.log.ids_active_listings
        else:
            return False

    #ver se algum item nas active_listings vendeu
    #retorna uma nova active listings se sim
    #return a active listings se nao
    def seeifanyitemsold(self):

        active_listings = self.getactivelistingsparsed()
        if active_listings != False:
            if self.log.ids_active_listings != active_listings:
                self.log.writenewactivelistings(active_listings)
                print 'VENDI ITEMS!'
                return True
        else:
            print "ERROR"
            return False

    #todo
    def selltestfirst(self,item_name,id,price):
        sell_response = self.http.sellitem(id,price)
        if sell_response[0] is 200:
            while True:
                host = random.choice(self.log.list_hosts)
                recent_response = self.http.urlqueryrecentwithcountry(host,'US',0)
                item_response = self.http.urlqueryspecificitemind(host,item_name)

                if type(recent_response) is dict:
                    pass
                if type(item_response) is dict:
                    pass

    #Searches for kennyS cooblestone cases on the newly listed
    #If it finds one it trys to buy it if not nothing happens
    def searchkenny(self,recent):
        try:
            if recent.has_key('assets'):
                if recent['assets'].has_key('730'):

                    for item_id in recent['assets']['730']['2']:
                        if recent['assets']['730']['2'][item_id]['market_hash_name'] \
                                == 'ESL One Cologne 2015 Cobblestone Souvenir Package':

                            if 'Kenny' in recent['assets']['730']['2'][item_id]['descriptions']['2']['value']:

                                for listing_id in recent['listinginfo']:
                                    if recent['listinginfo'][listing_id]['asset']['id'] == item_id:

                                        if int(recent['listinginfo'][listing_id]['converted_currencyid']) == 2003:

                                            if int(recent['listinginfo'][listing_id]['converted_fee']) + \
                                                int(recent['listinginfo'][listing_id]['converted_price']) <= 70000:

                                                if recent['listinginfo'][listing_id]['listingid'] != self.last_listing_buy:

                                                    self.last_listing_buy_lock.acquire()
                                                    self.last_listing_buy = recent['listinginfo'][listing_id]['listingid']
                                                    self.last_listing_buy_lock.release()

                                                    print 'Estou prestes a entrar no acquire dos buys ON THREAD ' + str(0)
                                                    self.buy_lock.acquire()
                                                    try:
                                                        print 'Entrei no acquire dos buys ON THREAD '  + str(0)

                                                        temp = self.http.buyitem(recent['listinginfo'][listing_id]['listingid'],
                                                                                 recent['listinginfo'][listing_id]['converted_price'],
                                                                                 recent['listinginfo'][listing_id]['converted_fee'],
                                                                                 recent['listinginfo'][listing_id]['converted_currencyid'])

                                                        self.log.writetobuyfile(self.http.httputil.data_buy['subtotal'],
                                                                                self.http.httputil.data_buy['fee'],
                                                                                self.http.httputil.data_buy,
                                                                                recent['listinginfo'][listing_id]['listingid'],
                                                                                recent['assets']['730']['2']
                                                                                [item_id]['market_hash_name']
                                                                                ,temp[0],temp[1],0)
                                                        self.buy_lock.release()
                                                        print 'sai do lock dos buys ON THREAD ' + str(0)
                                                    except:
                                                        print "something went wrong buying a kennys case, fuck me!"
                                                        self.buy_lock.release()
        except (ValueError,KeyError):
            print "Error in the kennyS function!"


#----------------------------------------------THREADING-----------------------------------------------------------

    #Gets the retrieved JSON all ready for the buying routine
    def getfinallistfromrecent(self,recent_full):
        temp_full = self.getRecentTotalReady(recent_full)
        temp1_assets = self.getCleanAssetList(temp_full)
        temp2_assets = self.getlistassets(temp1_assets)
        temp1_listings = self.delNonCsgoListings(temp_full)
        temp2_listings = self.getCleanListinginfoListWithAsset(temp1_listings)
        temp3_listings = self.getcleanlistings(temp2_listings)
        temp4_listings = self.getlistlistings(temp3_listings)
        temp_final = self.getfinalrecentlist(temp2_assets,temp4_listings)
        return temp_final

    #This function is a thread
    def recentthread(self,http_interval,name):
        counter = 0
        times = []
        while True:
            time.sleep(http_interval)

            if self.dif_hosts == 'yes':
                if self.dif_countries == 'yes':
                    recent = self.queryrecentdifhostsdifcountries(name)
                else:
                    recent = self.queryrecentdifhosts(name)

            elif self.dif_hosts == 'no':
                if self.dif_countries == 'yes':
                    recent = self.queryrecentdifcountries(name)
                else:
                    recent = self.queryrecent(name)

            if recent[0] == False:
                print "CONN REFUSED ON THREAD " + str(name) +", sleeping..."
                time.sleep(30)
                pass

            elif recent[0] == -1:
                    time.sleep(http_interval)

            elif recent[0] == -2:
                    sleepe = random.randint(16,31)
                    print 'TIMEOUT NA THREAD ' + str(name) + ' SLEEPING FOR ' + str(sleepe) + ' SECS'
                    time.sleep(sleepe)

            elif type(recent[0]) == dict:
                buygoodresp = self.buyingroutine(self.getfinallistfromrecent(recent[0]),name,recent[1])

                if buygoodresp[0] is True:

                    id_item_pos_one = self.getpositiononeiteminv()

                    lowest_price = self.getlowestprice(buygoodresp[2])

                    if ((float(lowest_price)+(0.02*float(lowest_price)))/float(buygoodresp[3])) >= 1.07:
                        price_sell = float(lowest_price)
                        price_sell_str = "{0:.2f}".format(price_sell)
                        print price_sell
                    else:
                        price_sell = float(buygoodresp[1] * 0.94)
                        price_sell_str = "{0:.2f}".format(price_sell)
                        print price_sell

                    price_sell_without_fee = price_sell/1.15
                    print price_sell_without_fee
                    sell_response = self.sellitem(id_item_pos_one,float(price_sell_without_fee))

                    print 'Estou prestes a entrar no acquire dos sells on THREAD ' + str(name)
                    self.sell_lock.acquire()
                    print 'entrei no lock dos sells'

                    if sell_response[0] == 200:
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],
                                                 price_sell_str,name,price_sell_without_fee)
                    elif sell_response[0] == 502:
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],
                                                 price_sell_str,name,price_sell_without_fee)

                    self.sell_lock.release()
                    print 'sai do lock dos sells ON THREAD ' + str(name)

                counter += 1
                if counter % 10 == 0:
                    print 'A THREAD ' + str(name) + ' ESTA OK!!!!!!!!!!!!!!!!!!!!!!'

                elif counter % 250 == 0:
                    self.write_active_listings_lock.acquire()
                    if self.seeifanyitemsold():
                        self.parsewalletbalanceandwrite()
                    self.write_active_listings_lock.release()
                    print "CHEGUEI AS " + str(counter) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    time.sleep(random.randint(10,20))

            else:
                counter += 1
                if counter % 10 == 0:
                    print 'A THREAD ' + str(name) + ' ESTA OK!!!!!!!!!!!!!!!!!!!!!!'

                elif counter % 250 == 0:
                    self.write_active_listings_lock.acquire()
                    if self.seeifanyitemsold():
                        self.parsewalletbalanceandwrite()
                    self.write_active_listings_lock.release()
                    print "CHEGUEI AS " + str(counter) + ' SLEEPING NOW!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
                    time.sleep(random.randint(10,20))

                time.sleep(http_interval)


    def executethreads(self,n_threads,http_interval):
        list_threads = []

        for i in range(1,int(n_threads)+1):
            name = i
            t = threading.Thread(target=self.recentthread, args=(http_interval,name))
            t.start()
            list_threads.append(t)

        while True:
            for thread in list_threads:
                if not thread.is_alive():
                    list_threads.remove(thread)
                    print "Removed thread " + str(thread)
            time.sleep(900)