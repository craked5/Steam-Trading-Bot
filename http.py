#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

import requests as req
import ast
import ujson
import time
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from http_util import Httpheaders

class SteamBotHttp:

    def __init__(self):
        self.httputil = Httpheaders()
        self.down_state = 0
        self.host = 'steamcommunity.com'
        self.pre_host_normal = 'http://'
        self.pre_host_https = 'https://'
        self.market = '/market'
        #currency=3 == euro
        self.item_price_viewer = '/priceoverview/?currency=3&appid=730&market_hash_name='
        self.recent_listed = '/recent/?country=PT&language=english&currency=3'
        self.complete_url_item = self.pre_host_normal+self.host+self.market+self.item_price_viewer
        self.complete_url_recent = self.pre_host_normal+self.host+self.market+self.recent_listed
        self.sell_item_url = self.pre_host_https+self.host+self.market+'/sellitem/'
        self.buy_item_url_without_listingid = self.pre_host_https+self.host+self.market+'/buylisting/'
        self.render_item_url_first_part = self.pre_host_normal+self.host+self.market+'/listings/730/'
        self.render_item_url_sencond_part = '/render/?currency=3'
        self.recent_compare = {}

    def login(self):

        donotcache = self.now_milliseconds()

        self.httputil.rsa_data['donotcache'] = donotcache
        self.httputil.login_data['donotcache'] = donotcache

        temp_rsa = req.post('https://steamcommunity.com/login/getrsakey/', headers=self.httputil.rsa_headers, data=self.httputil.rsa_data)
        print temp_rsa.content
        print 'O status code do GETRSA foi ' + str(temp_rsa.status_code)

        temp_ras_good = ujson.loads(temp_rsa.content)
        self.httputil.login_data['rsatimestamp'] = temp_ras_good['timestamp']
        mod = long(temp_ras_good['publickey_mod'], 16)
        exp = long(temp_ras_good['publickey_exp'], 16)
        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.PKCS115_Cipher(rsa_key)
        encrypted_password = rsa.encrypt(self.httputil.password)
        encrypted_password = base64.b64encode(encrypted_password)
        self.httputil.login_data['password'] = encrypted_password

        temp_dologin = req.post('https://steamcommunity.com/login/dologin/', headers=self.httputil.rsa_headers, data=self.httputil.login_data)
        print temp_dologin.content
        print 'O status code do DOLOGIN foi ' + str(temp_dologin.status_code)

        temp_dologin_good = ujson.loads(temp_dologin.content)
        self.httputil.transfer_data['steamid'] = temp_dologin_good['transfer_parameters']['steamid']
        self.httputil.transfer_data['token'] = temp_dologin_good['transfer_parameters']['token']
        self.httputil.transfer_data['auth'] = temp_dologin_good['transfer_parameters']['auth']
        self.httputil.transfer_data['remember_login'] = temp_dologin_good['transfer_parameters']['remember_login']
        self.httputil.transfer_data['token_secure'] = temp_dologin_good['transfer_parameters']['token_secure']

        temp_transfer = req.post('https://store.steampowered.com/login/transfer', headers=self.httputil.transfer_headers,data=self.httputil.transfer_data)
        print 'O status code do LOGINTRANSFER foi ' + str(temp_transfer.status_code)

    def logout(self):
        temp_logout = req.post('https://steamcommunity.com/login/logout/', headers= self.httputil.headers_logout, data= self.httputil.logout_data)
        print 'O status code do LOGOUT FOR ' + str(temp_logout.status_code)


    def now_milliseconds(self):
        self.donotcache = int(time.time() * 1000)

    def urlQueryItem(self,item):

        steam_response = req.get(self.complete_url_item + item, headers=self.httputil.headers_recent_anditem)
        if steam_response.status_code == 200:
            try:
                item_temp = ujson.loads(steam_response.content)
            except ValueError:
                return steam_response.status_code, steam_response.content
            return item_temp
        else:
            return steam_response.status_code

    def urlQueryRecent(self,host,thread):
        try:

            steam_response = req.get(self.complete_url_recent.replace(self.host,host),headers=self.httputil.headers_recent)

            if steam_response.status_code == 200:
                print 'Status code: ' + str(steam_response.status_code) + ' na thread ' + str(thread)
                timestamp = time.time()
                time_temp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))
                self.httputil.headers_recent['If-Modified-Since'] = time_temp
                try:
                    recent_temp = ujson.loads(steam_response.text)
                except ValueError:
                    return False
                return recent_temp

            elif steam_response.status_code == 304:
                print 'Status code: ' + str(steam_response.status_code) + ' na thread ' + str(thread)
                return -1

        except req.ConnectionError:
            return False

    def urlqueryspecificitemind(self,host,item):

        try:
            steam_response = req.get(self.render_item_url_first_part.replace(self.host,host)+item+self.render_item_url_sencond_part,
                                     headers = self.httputil.headers_item_list_ind)
            print steam_response.url
        except req.ConnectionError:
            return False

        except req.Timeout, req.ReadTimeout:
            print "shit i got a timeout"
            return False

        if steam_response.status_code == 429:
            return False
        else:
            try:
                recent_temp = ujson.loads(steam_response.text)
            except ValueError:
                return False

        return recent_temp

    def getpositiononeiteminv(self):

        temp_inv = req.get('http://steamcommunity.com/id/craked5/inventory/json/730/2/')
        array = ujson.loads(temp_inv.content)

        for key in array['rgInventory']:
            if array['rgInventory'][key]['pos'] == 1:
                temp_id = array['rgInventory'][key]['id']
                return temp_id

        return False

    #price = ao preco que eu quero receber
    #price vem em float
    def sellitem(self,assetid,price):

        list_return = []
        price_temp = price * 100
        price_temp = (0.90*price_temp)
        price_temp = round(price_temp)

        self.httputil.data_sell['assetid'] = int(assetid)
        self.httputil.data_sell['price'] = int(price_temp)

        temp = req.post(self.sell_item_url, data=self.httputil.data_sell, headers=self.httputil.headers_sell)

        list_return.append(temp.status_code)
        list_return.append(temp.content)
        list_return.append(int(price_temp))

        return list_return

    def buyitem(self,listing,subtotal,fee,currency):

        temp_tuple = []

        self.httputil.data_buy['currency'] = int(currency) - 2000
        self.httputil.data_buy['subtotal'] = int(subtotal)
        self.httputil.data_buy['fee'] = int(fee)
        self.httputil.data_buy['total'] = int(self.httputil.data_buy['subtotal'] + self.httputil.data_buy['fee'])
        try:
            temp = req.post(self.buy_item_url_without_listingid+listing, data=self.httputil.data_buy, headers=self.httputil.headers_buy)
        except req.ConnectionError:
            pass

        temp_tuple.append(int(temp.status_code))
        temp_tuple.append(ast.literal_eval(temp.content))

        return temp_tuple

#-----------------------------------------AUX FUNCTIONS------------------------------------------------------------------

    def queryitemtest(self):

        steam_response = req.get(self.render_item_url_first_part+'AWP%20%7C%20Asiimov%20%28Field-Tested%29'+self.render_item_url_sencond_part,
                                 headers = self.httputil.headers_item_list_ind)

        print steam_response.status_code
        print steam_response.url

        recent_temp = ujson.loads(steam_response.text)
        return recent_temp

