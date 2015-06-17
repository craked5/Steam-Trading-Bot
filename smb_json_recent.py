#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import json
import ujson
import decimal
from smb_logic import Logic
from smb_requests_recent import SteamBotHttp


class SteamJsonRecent:

    def __init__(self):
        self.recent_parsing_list = [u'results_html',u'hovers',u'last_listing',u'last_time',u'app_data',u'currency',
                                    u'success',u'more',u'purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount','status','original_amount','tradable',
                                   'background_color','icon_url','icon_url_large','descriptions','name','name_color','type',
                                   'market_name','market_actions','commodity','app_icon','owner','actions','market_tradable_restriction']
        self.listinginfo_parsing_list = ['fee','publisher_fee_percent','currencyid','steam_fee','publisher_fee',
                                         'converted_currencyid','converted_steam_fee','converted_publisher_fee','converted_price_per_unit',
                                         'converted_fee_per_unit','converted_fee_per_unit','converted_publisher_fee_per_unit','price',
                                         'publisher_fee_app','converted_steam_fee_per_unit']
        self.listinginfo_asset_parsing_list = ['currency','contextid','amount','market_actions','appid']
        self.listinginfo_list = {}
        self.final_list_listings = {}
        self.final_list_assets = {}
        self.final_list = {}
        self.float100 = float(100)
        self.http = SteamBotHttp()
        self.log = Logic()

    def getRecentTotalReady(self, recent_full):
        self.recent_parsed = {}
        for key in self.recent_parsing_list:
            if key != None:
                if key in recent_full:
                    recent_full.pop(key)
        #retorna um dict so com as keys assets e listinginfo
        self.recent_parsed = recent_full

#-------------------------------------------ASSETS!!!!!!!!!!!!!!---------------------------------------------------
    #NAO EXECUTAR MANUALMENTE!!!!!!!!!!!!!!!!!!!!
    def getCleanAssetList(self):
        self.asset_list = {}
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

    #lista final dos assets = list2 = {'awp worm god':'231342342','ak47 redline':'432342342342',...}
    #nao executar, so no getfinallist()
    def getlistassets(self):
        try:
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
        temp_list = self.recent_parsed['listinginfo']
        self.listinginfo_list = temp_list
        for k in self.listinginfo_list.keys():
            if self.listinginfo_list[k]['asset']['appid'] != 730:
                self.listinginfo_list.pop(k)
            elif self.listinginfo_list[k]['asset']['amount'] == 0:
                self.listinginfo_list.pop(k)

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

        self.delNonCsgoListings()
        self.getCleanListinginfoListWithAsset()
        self.getcleanlistings()
        for key_item in self.listinginfo_list.keys():
            if self.listinginfo_list[key_item].has_key('converted_price'):
                self.listinginfo_list[key_item]['converted_price'] = float(self.listinginfo_list[key_item]['converted_price']) / self.float100
                self.listinginfo_list[key_item]['converted_fee'] = float(self.listinginfo_list[key_item]['converted_fee']) / self.float100
            else:
                self.listinginfo_list.pop(key_item)
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
        print self.final_list
        return self.final_list

    def seeifrecentiteminlistbuy(self,item):
        for temp in self.log.list_items_to_buy:
            if item == temp:
                return True

    def seeifbuyinggoodandsell(self):
        for key in self.final_list:
            if self.seeifrecentiteminlistbuy(key) == True:
                temp_item_priceover = self.http.urlQueryItem(key)
                temp_item_priceover['success']
                if temp_item_priceover['success'] == True:
                    for key_in_priceover in temp_item_priceover:
                        if isinstance(temp_item_priceover[key_in_priceover], basestring):
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].rstrip('&#8364; ')
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace(',','.')
                            print temp_item_priceover[key_in_priceover]
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace('-','0')
                            temp_item_priceover[key_in_priceover] = float(temp_item_priceover[key_in_priceover])
                    print self.final_list[key]
                    print temp_item_priceover['median_price']
                    try:
                        if float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price'])) >= float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100))):
                            print temp_item_priceover['median_price']
                            print self.final_list[key]
                            print float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price']))
                            print float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100)))
                            print "podia ter comprado " + key
                            return True
                            break
                        else:
                            print temp_item_priceover['median_price']
                            print self.final_list[key]
                            print float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price']))
                            print float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100)))
                            print "nao posso comprar " + key
                            return False
                            break
                    except ValueError:
                        print "float not valid"
                    except:
                        print "error"

    def seeifbuyinggoodnosell(self):
        for key in self.final_list:
            if self.seeifrecentiteminlistbuy(key) == True:
                temp_item_priceover = self.http.urlQueryItem(key)
                temp_item_priceover['success']
                if temp_item_priceover['success'] == True:
                    for key_in_priceover in temp_item_priceover:
                        if isinstance(temp_item_priceover[key_in_priceover], basestring):
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].rstrip('&#8364; ')
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace(',','.')
                            print temp_item_priceover[key_in_priceover]
                            temp_item_priceover[key_in_priceover] = temp_item_priceover[key_in_priceover].replace('-','0')
                            temp_item_priceover[key_in_priceover] = float(temp_item_priceover[key_in_priceover])
                    print self.final_list[key]
                    print temp_item_priceover['median_price']
                    try:
                        if float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price'])) >= float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100))):
                            print temp_item_priceover['median_price']
                            print self.final_list[key]
                            print float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price']))
                            print float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100)))
                            print "podia ter comprado " + key
                            return True
                            break
                        else:
                            print temp_item_priceover['median_price']
                            print self.final_list[key]
                            print float("{0:.2f}".format(temp_item_priceover['median_price'] - self.final_list[key]['converted_price']))
                            print float("{0:.2f}".format(((20*temp_item_priceover['median_price']) / 100)))
                            print "nao posso comprar " + key
                            return False
                            break
                    except ValueError:
                        print "float not valid"

    def buyitem(self):
        pass

#--------------------------------------AUX FUNCTIONS------------------------------------------------

    def exportJsonToFile(self,json):
        with open('/Users/nunosilva/Desktop/steamutils/data.txt', 'w') as outfile:
            ujson.dump(json, outfile)
        return json