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

    def __init__(self):
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
        self.http = SteamBotHttp()
        #logic mode recent
        #logic mode item
        self.log = Logic('recent')
        self.last_listing_buy = ''
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

    def getRecentTotalReady(self, recent_full):
        self.recent_parsed = {}
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

    def seeifbuyinggood(self,final_list,t_name):
        temp_resp = []
        if final_list == False:
            temp_resp.append(False)
            return temp_resp
        else:
            final_list_this = final_list
            for key in final_list_this:
                if key in self.log.list_items_to_buy:
                    print key
                    if self.list_median_prices.has_key(key):
                        print self.list_median_prices[key]
                        #try:
                        temp_converted_price_math = float(decimal.Decimal(final_list_this[key]['converted_price'])/100)
                        temp_converted_fee_math = float(decimal.Decimal(final_list_this[key]['converted_fee'])/100)
                        if float(float("{0:.2f}".format(self.list_median_prices[key])) -
                                float((temp_converted_price_math+temp_converted_fee_math))) >= \
                                (30.5*(temp_converted_price_math+temp_converted_fee_math)/100):
                            if (temp_converted_price_math+temp_converted_fee_math) <= float((80*self.getwalletbalance())):
                                if int(final_list_this[key]['converted_currencyid']) == 2003:
                                    if final_list_this[key]['listingid'] != self.last_listing_buy:
                                        self.last_listing_buy_lock.acquire()
                                        self.last_listing_buy = final_list_this[key]['listingid']
                                        self.last_listing_buy_lock.release()
                                        print 'Estou prestes a entrar no acquire dos buys ON THREAD ' + str(t_name)
                                        self.buy_lock.acquire()
                                        print 'Entrey no acquire dos buys ON THREAD '  + str(t_name)
                                        temp = self.http.buyitem(final_list_this[key]['listingid'],
                                                                 final_list_this[key]['converted_price'],
                                                                 final_list_this[key]['converted_fee'],
                                                                 final_list_this[key]['converted_currencyid'])
                                        self.log.writetobuyfile(self.http.httputil.data_buy['subtotal'],
                                                                self.http.httputil.data_buy['fee'],
                                                             self.http.httputil.data_buy,final_list_this[key]['listingid'],
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
                                                    self.buy_lock.release()
                                                    print 'sai do lock dos buys ON THREAD ' + str(t_name)
                                                    return temp_resp
                                        else:
                                            print "Nao pude comprar item " + key
                                            print "erro ao comprar item"
                                        self.buy_lock.release()
                                        print 'sai do lock dos buys ON THREAD ' + str(t_name)
                                    else:
                                        temp_resp.append(False)
                                        return temp_resp
                            else:
                                print "Nao pude comprar: " + key +" porque nao tenho fundos On THREAD " + str(t_name)
                        else:
                            print "nao posso comprar " + key + " porque margens nao sao suficientes ON THREAD " + str(t_name)
                        #except ValueError, KeyError:
                            #print "float not valid, or some key does not exist"
                            #temp_resp.append(False)
                            #return temp_resp
                    else:
                        temp_resp.append(False)
                        return temp_resp
        temp_resp.append(False)
        return temp_resp

#----------------------------------------------AUX FUNCTIONS-----------------------------------------------------------
    def urlqueryrecent(self,thread):
        return self.http.urlQueryRecent('steamcommunity.com',thread)

    def urlQueryRecentdifhosts(self,thread):
        host = random.choice(self.log.list_hosts)
        return self.http.urlQueryRecent(host,thread)

    def getpositiononeiteminv(self):
        return self.http.getpositiononeiteminv()

    def sellitem(self,assetid,price):
        return self.http.sellitem(assetid,price)

    def exportJsonToFile(self,json):
        with open('util/median_prices.json', 'w') as outfile:
            ujson.dump(json, outfile)
        outfile.close()
        return json

    def writeInItemsTxt(self,item):
        return self.log.writeInItemsTxt(item)

    def delInItemsTxt(self,item):
        return self.log.delInItemsTxt(item)

    def getlistbuyitems(self):
        return self.log.list_items_to_buy

    def getwalletbalance(self):
        return float(self.log.wallet_balance)

    def loadmedianpricesfromfile(self):
        file = open('util/median_prices.json','r')
        self.list_median_prices = ujson.load(file)
        file.close()
        return self.list_median_prices

    def writetosellfile(self,status,content,item,price,balance,thread_n):
        return self.log.writetosellfile(status,content,item,price,balance,thread_n)

    def writetobuyfile(self,subtotal,fee,data_buy,listingid,key,responsecode,responsedict,thread_n):
        return self.log.writetobuyfile(subtotal,fee,data_buy,listingid,key,responsecode,responsedict,thread_n)

    def sellitemtest(self,assetid,price):
        return self.http.sellitem(assetid,price)

    def writetowalletadd(self,amount_add):
        temp = float(amount_add) + float(self.getwalletbalance())
        temp = temp*100
        return self.log.writetowallet(int(temp))

    def buyitemtest(self,name,listing,subtotal,fee,currency):
        temp =  self.http.buyitem(listing,subtotal,fee,currency)
        self.writetobuyfile(subtotal,fee,self.http.httputil.data_buy,listing,name,temp[0],temp[1])
        self.log.writetowallet(temp[1]['wallet_info']['wallet_balance'])
        temp_id = self.getpositiononeiteminv()
        temp_sell = self.sellitemtest(temp_id,0.01)
        if temp_sell[0] == 200:
            self.writetosellfile(temp_sell[0],temp_sell[1],name,0.01,self.getwalletbalance())
            self.writetowalletadd(0.01)
            print "balance esperado depois desta sale: " + str(self.getwalletbalance())
        elif temp_sell[0] == 502:
            self.writetosellfile(temp_sell[0],temp_sell[1],name,0.01,self.getwalletbalance())

    def getmedianitemlist(self):

        self.list_median_prices = {}

        for key in self.log.list_items_to_buy:
            temp_item_priceover = {}
            temp_item_priceover = self.http.urlQueryItem(key)
            if type(temp_item_priceover) == int:
                print "Erro ao obter preco medio de " + key
                print "Status code da querie: " + str(temp_item_priceover)

            elif temp_item_priceover.has_key('median_price'):
                temp_median_price = temp_item_priceover['median_price']
                if isinstance(temp_median_price, basestring):
                    temp_median_price = temp_median_price.replace('&#8364; ','').replace(',','.').replace('-','0')
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
            balance_str = balance_soup.encode('ascii','ignore').replace(',','.')

            return float(balance_str)
        else:
            print "ERROR GETTING WALLET BALANCE, MAYBE FAZER LOGIN RESOLVE ESTE PROBLEMA"
            return False


    #Vai buscar o valor o balance da minha carteira ao Steam diretamente
    #e se encontrar, atualiza a var wallet_balance
    def parsewalletbalanceandwrite(self):

        soup = BeautifulSoup(self.http.getsteamwalletsite(),'html.parser')
        balance_soup = soup.find('span',{'id':'marketWalletBalanceAmount'})

        if balance_soup != None:
            balance_soup = balance_soup.get_text()
            balance_str = balance_soup.encode('ascii','ignore').replace(',','.')

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
#----------------------------------------------THREADING-----------------------------------------------------------

    def callfuncs(self,recent_full):
        temp_full = self.getRecentTotalReady(recent_full)
        temp1_assets = self.getCleanAssetList(temp_full)
        temp2_assets = self.getlistassets(temp1_assets)
        temp1_listings = self.delNonCsgoListings(temp_full)
        temp2_listings = self.getCleanListinginfoListWithAsset(temp1_listings)
        temp3_listings = self.getcleanlistings(temp2_listings)
        temp4_listings = self.getlistlistings(temp3_listings)
        temp_final = self.getfinalrecentlist(temp2_assets,temp4_listings)
        return temp_final

    def onerecentthread(self,http_interval,name):
        counter = 0
        times = []
        while True:
            time.sleep(http_interval)
            #start = time.time()

            if self.dif_hosts == 'yes':
                recent = self.urlQueryRecentdifhosts(name)
                #if type(recent) == list:
                    #self.timestamp_lock.acquire()
                    #self.timestamp = recent[0]
                    #self.timestamp_lock.release()

            elif self.dif_hosts == 'no':
                recent = self.urlqueryrecent(name)
                #if type(recent) == list:
                    #self.timestamp_lock.acquire()
                    #self.timestamp = recent[0]
                    #self.timestamp_lock.release()

            if recent == False:
                print "CONN REFUSED ON THREAD " + str(name) +", sleeping..."
                time.sleep(30)
                pass

            elif recent == -1:
                    time.sleep(http_interval)

            elif type(recent) == dict:
                final = self.callfuncs(recent)
                buygoodresp = self.seeifbuyinggood(final,name)
                #print "A resposta do seeifbuyinggood() foi "
                #print buygoodresp
                if buygoodresp[0] is True:
                    price_sell = buygoodresp[1]
                    price_sell = float(price_sell*0.90)
                    price_sell = "{0:.2f}".format(price_sell)
                    temp_item_one = self.getpositiononeiteminv()
                    sell_response = self.sellitem(temp_item_one,buygoodresp[1])
                    print 'Estou prestes a entrar no acquire dos sells on THREAD ' + str(name)
                    self.sell_lock.acquire()
                    print 'entrei no lock dos sells'
                    if sell_response[0] == 200:
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],
                                                 price_sell,self.getwalletbalance(),name)
                    elif sell_response[0] == 502:
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],
                                                 price_sell,self.getwalletbalance(),name)
                    self.sell_lock.release()
                    print 'sai do lock dos sells ON THREAD ' + str(name)
                counter += 1
                if counter % 10 == 0:
                    print 'A THREAD ' + str(name) + ' ESTA OK!!!!!!!!!!!!!!!!!!!!!!'
                elif counter % 300 == 0:
                    self.write_active_listings_lock.acquire()
                    if self.seeifanyitemsold() == True:
                        self.parsewalletbalanceandwrite()
                    self.write_active_listings_lock.release()
                elif counter % 4000 == 0:
                    time.sleep(60)
                time.sleep(http_interval)
                #elapsed = time.time()
                #elapsed = elapsed - start
                #times.append(elapsed)
                #print elapsed

            else:
                counter += 1
                if counter % 10 == 0:
                    print 'A THREAD ' + str(name) + ' ESTA OK!!!!!!!!!!!!!!!!!!!!!!'
                elif counter % 300 == 0:
                    self.write_active_listings_lock.acquire()
                    if self.seeifanyitemsold() == True:
                        self.parsewalletbalanceandwrite()
                    self.write_active_listings_lock.release()
                elif counter % 4000 == 0:
                    time.sleep(60)
                time.sleep(http_interval)
                #print i
                #elapsed = time.time()
                #elapsed = elapsed - start
                #times.append(elapsed)
                #print elapsed


    def executethreads(self,n_threads,http_interval):
        i = 1
        list_threads = []

        for i in range(1,int(n_threads)+1):
            name = i
            t = threading.Thread(target=self.onerecentthread, args=(http_interval,name))
            t.start()
            list_threads.append(t)
