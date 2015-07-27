'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

import time
import unicodedata
from bs4 import BeautifulSoup
import ujson
import decimal
import random
from logic import Logic
from http import SteamBotHttp



class SteamJsonRecent:

    def __init__(self):
        self.recent_parsing_list = [u'results_html',u'hovers',u'last_listing',u'last_time',u'app_data',u'currency',
                                    u'success',u'more',u'purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount',
                                   'status','original_amount','tradable',
                                   'background_color','icon_url','icon_url_large','descriptions',
                                   'name','name_color','type',
                                   'market_name','market_actions','commodity','app_icon','owner',
                                   'actions','market_tradable_restriction']
        self.listinginfo_parsing_list = ['fee','publisher_fee_percent','steam_fee','publisher_fee',
                                         'converted_steam_fee','converted_publisher_fee','converted_price_per_unit',
                                         'converted_fee_per_unit','converted_fee_per_unit',
                                         'converted_publisher_fee_per_unit','price',
                                         'publisher_fee_app','converted_steam_fee_per_unit']
        self.listinginfo_asset_parsing_list = ['currency','contextid','amount','market_actions','appid']
        self.list_median_prices = {}
        self.listinginfo_list = {}
        self.final_list_listings = {}
        self.final_list_assets = {}
        self.final_list = {}
        self.float100 = float(100)
        self.http = SteamBotHttp()
        #logic mode recent
        #logic mode item
        self.log = Logic('recent')
        self.dif_hosts = self.log.dif_hosts_recent
        self.contaSim = 0
        self.contaNao = 0

    def getRecentTotalReady(self, recent_full):

        self.recent_parsed = {}

        if type(recent_full) == dict:
            for key in self.recent_parsing_list:
                if recent_full.has_key(key):
                    recent_full.pop(key)
        else:
            recent_full = {}

        #retorna um dict so com as keys assets e listinginfo
        self.recent_parsed = recent_full

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------ASSETS!!!!!!!!!!!!!!----------------------------------------------------

    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getCleanAssetList(self):

        self.asset_list = {}

        if self.recent_parsed.has_key('assets'):
            self.asset_list = self.recent_parsed['assets']
            if self.asset_list.has_key('730'):
                self.asset_list = self.asset_list['730']
                self.asset_list = self.asset_list['2']
                for key_item in self.asset_list:
                    for key in self.asset_parsing_list:
                        if key in self.asset_list[key_item]:
                            self.asset_list[key_item].pop(key)
            else:
                return False
        else:
            return False

    #lista final dos assets = list2 = {'awp worm god':'231342342','ak47 redline':'432342342342',...}
    #nao executar, so no getfinallist()
    def getlistassets(self):

        try:
            self.final_list_assets = {}
            self.getCleanAssetList()

            for key_item in self.asset_list.keys():
                if self.asset_list[key_item].has_key('market_hash_name'):
                    self.final_list_assets[self.asset_list[key_item]['market_hash_name']] \
                    = self.asset_list[key_item]['id']
            return True
        except:
            print "falha no parsing dos assets"
            return False

#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------LISTINGS!!!!!!!!!!!--------------------------------------------------------

    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    #1 a ser executada
    def delNonCsgoListings(self):

        self.listinginfo_list = {}

        if self.recent_parsed.has_key('listinginfo'):
            temp_list = self.recent_parsed['listinginfo']
            self.listinginfo_list = temp_list
            for k in self.listinginfo_list.keys():
                if self.listinginfo_list[k]['asset']['appid'] != 730:
                    self.listinginfo_list.pop(k)
                elif self.listinginfo_list[k]['asset']['amount'] == 0:
                    self.listinginfo_list.pop(k)
        else:
            return False

    #2 a ser executada
    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getCleanListinginfoListWithAsset(self):

        for key_item in self.listinginfo_list:
            for key in self.listinginfo_parsing_list:
                if self.listinginfo_list[key_item].has_key(key):
                    self.listinginfo_list[key_item].pop(key)

    #3 a ser executada
    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getcleanlistings(self):

        for key_item in self.listinginfo_list:
            for key in self.listinginfo_asset_parsing_list:
                if self.listinginfo_list[key_item]['asset'].has_key(key):
                    self.listinginfo_list[key_item]['asset'].pop(key)

    #lista final dos listings: list1 = {'231342342':'2.45','432342342342':'12.76',...
    #nao executar, so no getfinallist()
    def getlistlistings(self):
        self.final_list_listings = {}

        if self.delNonCsgoListings() != False:
            self.getCleanListinginfoListWithAsset()
            self.getcleanlistings()
            for key_item in self.listinginfo_list.keys():
                if self.listinginfo_list[key_item].has_key('converted_price'):
                    self.listinginfo_list[key_item]['converted_price']
                    self.listinginfo_list[key_item]['converted_fee']
                else:
                    self.listinginfo_list.pop(key_item)
        else:
            return False

#-------------------------------------------------------------------------------------------------------------------

    def getfinalrecentlist(self):

        self.final_list = {}

        if self.getlistlistings() == False:
            print 'falha no parsing dos listings, try again'
            return False

        elif self.getlistassets() == False:
            print 'falha no parsing dos assets, try again'
            return False

        else:
            for k in self.listinginfo_list:
                for k2 in self.final_list_assets:
                    if self.final_list_assets.get(k2) == self.listinginfo_list[k]['asset']['id']:
                        self.final_list[k2] = self.listinginfo_list.get(k)

        return self.final_list

    def seeifbuyinggood(self):

        temp_resp = []

        for key in self.final_list:
            if key in self.log.list_items_to_buy:
                print key
                if self.list_median_prices.has_key(key):
                    print self.list_median_prices[key]
                    #try:
                    temp_converted_price_math = float(decimal.Decimal(self.final_list[key]['converted_price'])/100)
                    temp_converted_fee_math = float(decimal.Decimal(self.final_list[key]['converted_fee'])/100)
                    if float(float("{0:.2f}".format(self.list_median_prices[key])) -
                            float((temp_converted_price_math+temp_converted_fee_math))) >= \
                            (29.5*(temp_converted_price_math+temp_converted_fee_math)/100):
                        if (temp_converted_price_math+temp_converted_fee_math) <= float((80*self.getwalletbalance())):
                            if int(self.final_list[key]['converted_currencyid']) == 2003:
                                temp = {}
                                temp = self.http.buyitem(self.final_list[key]['listingid'],
                                                         self.final_list[key]['converted_price'],
                                                         self.final_list[key]['converted_fee'],
                                                         self.final_list[key]['converted_currencyid'])
                                self.log.writetobuyfile(self.http.httputil.data_buy['subtotal'],
                                                        self.http.httputil.data_buy['fee'],
                                                     self.http.httputil.data_buy,
                                                        self.final_list[key]['listingid'],key,temp[0],temp[1],0)
                                if temp[0] == 200:
                                    if temp[1]['wallet_info'].has_key('wallet_balance'):
                                        if self.log.writetowallet(temp[1]['wallet_info']['wallet_balance']) == True:
                                            print "Ok COMPREI A: " + key + " ao preco: " + \
                                                  str(self.final_list[key]['converted_price'] +
                                                      self.final_list[key]['converted_fee'])
                                            temp_resp.append(True)
                                            temp_resp.append(self.list_median_prices[key])
                                            temp_resp.append(key)
                                            return temp_resp
                                else:
                                    print "Nao pude comprar item " + key
                                    print "erro ao comprar item"
                        else:
                            print "Nao pude comprar: " + key +" porque nao tenho fundos"
                    else:
                        print "nao posso comprar " + key + " porque margens nao sao suficientes"
                    #except ValueError, KeyError:
                        #print "float not valid, or some key does not exist"
                        #temp_resp.append(False)
                        #return temp_resp
        temp_resp.append(False)
        return temp_resp

#----------------------------------------------AUX FUNCTIONS-----------------------------------------------------------
    def urlqueryrecent(self):
        return self.http.urlQueryRecent('steamcommunity.com',0)

    def urlQueryRecentdifhosts(self):
        host = random.choice(self.log.list_hosts)
        return self.http.urlQueryRecent(host,0)

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

    def parsewalletbalanceandwrite(self):

        soup = BeautifulSoup(self.http.getsteamwalletsite(),'html.parser')
        balance_soup = soup.find('span',{'id':'marketWalletBalanceAmount'})

        if balance_soup != None:
            balance_soup = balance_soup.get_text()
            balance_str = balance_soup.encode('ascii','ignore').replace(',','.')

            self.log.writetowallet(float(balance_str)*100)

            print self.log.wallet_balance
            print float(balance_str)
            return float(balance_str)
        else:
            print "ERROR GETTING WALLET BALANCE, MAYBE FAZER LOGIN RESOLVE ESTE PROBLEMA"
            return False

    def getactivelistingsparsed(self):
        active_listings = self.http.getmyactivelistingsraw()
        active_listings_list = []

        print type(active_listings)
        if type(active_listings) == dict:
            if active_listings.has_key('assets'):
                if active_listings['assets'].has_key('730'):
                    active_listings = active_listings['assets']['730']['2']

                    for id in active_listings:
                        active_listings_list.append(id)

                    return active_listings_list
        else:
            return False

    #todo
    def seeifanyitemsold(self):

        active_listings = self.getactivelistingsparsed()






#----------------------------------------FUNCAO QUE EXECUTA AS OUTRAS TODAS---------------------------------------------

    def startbuyingsell(self,http_interval):
        i = 0
        times = []
        while True:
            if self.dif_hosts == 'yes':
                recent = self.urlQueryRecentdifhosts()
            elif self.dif_hosts == 'no':
                recent = self.urlqueryrecent()

            if recent == False:
                print "CONN REFUSED, sleeping..."
                time.sleep(30)
                pass
            elif recent == -1:
                    print "recent igual, trying again"
                    time.sleep(http_interval)
            elif type(recent) == dict:
                self.getRecentTotalReady(recent)
                self.getfinalrecentlist()
                buygoodresp = self.seeifbuyinggood()
                if buygoodresp[0] is True:
                    price_sell = buygoodresp[1]
                    price_sell = float(price_sell*0.90)
                    price_sell = "{0:.2f}".format(price_sell)
                    ID_item_pos_one = self.getpositiononeiteminv()
                    sell_response = self.sellitem(ID_item_pos_one,buygoodresp[1])
                    if sell_response[0] == 200:
                        self.writetowalletadd(price_sell)
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],price_sell,
                                                 self.getwalletbalance(),0)
                    elif sell_response[0] == 502:
                        self.log.writetosellfile(sell_response[0],sell_response[1],buygoodresp[2],price_sell,
                                                 self.getwalletbalance(),0)
                time.sleep(http_interval)
            else:
                time.sleep(http_interval)
                '''
