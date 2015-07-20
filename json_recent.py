#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

import ujson
import decimal
from logic import Logic
from httputil import SteamBotHttp



class SteamJsonRecent:

    def __init__(self):
        self.recent_parsing_list = [u'results_html',u'hovers',u'last_listing',u'last_time',u'app_data',u'currency',
                                    u'success',u'more',u'purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount','status','original_amount','tradable',
                                   'background_color','icon_url','icon_url_large','descriptions','name','name_color','type',
                                   'market_name','market_actions','commodity','app_icon','owner','actions','market_tradable_restriction']
        self.listinginfo_parsing_list = ['fee','publisher_fee_percent','steam_fee','publisher_fee',
                                         'converted_steam_fee','converted_publisher_fee','converted_price_per_unit',
                                         'converted_fee_per_unit','converted_fee_per_unit','converted_publisher_fee_per_unit','price',
                                         'publisher_fee_app','converted_steam_fee_per_unit']
        self.listinginfo_asset_parsing_list = ['currency','contextid','amount','market_actions','appid']
        self.listinginfo_list = {}
        self.final_list_listings = {}
        self.final_list_assets = {}
        self.final_list = {}
        self.float100 = float(100)
        self.http = SteamBotHttp()
        #logic mode recent
        #logic mode item
        self.log = Logic('recent')
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
                    #print type(self.listinginfo_list[key_item]['converted_price'])
                    #print self.listinginfo_list[key_item]['converted_price']
                    self.listinginfo_list[key_item]['converted_price']
                    self.listinginfo_list[key_item]['converted_fee']
                else:
                    self.listinginfo_list.pop(key_item)
        else:
            return False
        #except:
            #print "falha no parsing da lista de listings"
            #return False

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
        #print self.final_list
        return self.final_list

    def seeifrecentiteminlistbuy(self,item):
        for temp in self.log.list_items_to_buy:
            if item == temp:
                return True

    def seeifbuyinggood(self):
        temp_resp = []
        for key in self.final_list:
            if self.seeifrecentiteminlistbuy(key) == True:
                temp_item_priceover = {}
                temp_item_priceover = self.http.urlQueryItem(key)
                if temp_item_priceover['success'] == True:
                    for key_in_priceover in temp_item_priceover:
                        if isinstance(temp_item_priceover[key_in_priceover], basestring):
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].rstrip('&#8364; ')
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace(',','.')
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace('-','0')
                            if temp_item_priceover[key_in_priceover] != bool:
                                try:
                                    temp_item_priceover[key_in_priceover] = float(temp_item_priceover[key_in_priceover])
                                except ValueError:
                                    print "erro ao por em float"
                    try:
                        temp_converted_price_math = float(decimal.Decimal(self.final_list[key]['converted_price'])/100)
                        temp_converted_fee_math = float(decimal.Decimal(self.final_list[key]['converted_fee'])/100)
                        if float(float("{0:.2f}".format(temp_item_priceover['median_price'])) - float((temp_converted_price_math+temp_converted_fee_math))) >= \
                                (31.5*(temp_converted_price_math+temp_converted_fee_math)/100):
                            if (temp_converted_price_math+temp_converted_fee_math) <= float((80*self.getwalletbalance())):
                                if int(self.final_list[key]['converted_currencyid']) == 2003:
                                    temp = {}
                                    temp = self.http.buyitem(self.final_list[key]['listingid'],self.final_list[key]['converted_price'],
                                                             self.final_list[key]['converted_fee'],self.final_list[key]['converted_currencyid'])
                                    self.log.writetobuys(self.http.data_buy['subtotal'], self.http.data_buy['fee'],
                                                         self.http.data_buy,self.final_list[key]['listingid'],key,temp[0],temp[1])
                                    if temp[0] == 200:
                                        if temp[1]['wallet_info'].has_key('wallet_balance'):
                                            if self.log.writetowallet(temp[1]['wallet_info']['wallet_balance']) == True:
                                                print "Ok COMPREI A: " + key + " ao preco: " + \
                                                      str(self.final_list[key]['converted_price'] + self.final_list[key]['converted_fee'])
                                                temp_resp.append(True)
                                                #temp_resp.append(self.final_list[key]['listingid'])
                                                temp_resp.append(temp_item_priceover['median_price'])
                                                temp_resp.append(key)
                                                return temp_resp
                                    else:
                                        print "Nao pude comprar item " + key
                                        print "erro ao comprar item"
                            else:
                                print "Nao pude comprar: " + key +" porque nao tenho fundos"
                                #print "preco da arma: " + str(temp_converted_price_math+temp_converted_fee_math)
                                #print "saldo da wallet: " + str(self.log.wallet_balance)
                        else:
                            print "nao posso comprar " + key + " porque margens nao sao suficientes"
                            #print "preco da " + key + " : " + str(temp_converted_price_math+temp_converted_fee_math)
                            #print "preco medio da " + key + " : " + str(temp_item_priceover['median_price'])
                            #print "margem necessaria: " + str(20*(temp_converted_price_math+temp_converted_fee_math)/100)
                            #print "margem obtida: " + str((temp_item_priceover['median_price'] - (temp_converted_price_math+temp_converted_fee_math)))
                    except ValueError, KeyError:
                        print "float not valid, or some key does not exist"
                        temp_resp.append(False)
                        return temp_resp
        temp_resp.append(False)
        return temp_resp

#--------------------------------------AUX FUNCTIONS------------------------------------------------
    def urlQueryRecent(self):
        return self.http.urlQueryRecent()

    def getpositiononeiteminv(self):
        return self.http.getpositiononeiteminv()

    def sellitem(self,assetid,price):
        return self.http.sellitem(assetid,price)

    def exportJsonToFile(self,json):
        with open('stuff.txt', 'w') as outfile:
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
        return self.log.wallet_balance

    def writetosellfile(self,status,content,item,price,balance):
        return self.log.writetosells(status,content,item,price,balance)

    def writetobuyfile(self,subtotal,fee,data_buy,listingid,key,responsecode,responsedict):
        return self.log.writetobuys(subtotal,fee,data_buy,listingid,key,responsecode,responsedict)

    def sellitemtest(self,assetid,price):
        return self.http.sellitem(assetid,price)

    def writetowalletadd(self,amount_add):
        temp = float(amount_add) + float(self.getwalletbalance())
        temp = temp*100
        return self.log.writetowallet(int(temp))

    def buyitemtest(self,name,listing,subtotal,fee,currency):
        temp =  self.http.buyitem(listing,subtotal,fee,currency)
        self.writetobuyfile(subtotal,fee,self.http.data_buy,listing,name,temp[0],temp[1])
        self.log.writetowallet(temp[1]['wallet_info']['wallet_balance'])
        temp_id = self.getpositiononeiteminv()
        temp_sell = self.sellitemtest(temp_id,0.01)
        if temp_sell[0] == 200:
            self.writetosellfile(temp_sell[0],temp_sell[1],name,0.01,self.getwalletbalance())
            self.writetowalletadd(0.01)
            print "balance esperado depois desta sale: " + str(self.getwalletbalance())
        elif temp_sell[0] == 502:
            self.writetosellfile(temp_sell[0],temp_sell[1],name,0.01,self.getwalletbalance())

