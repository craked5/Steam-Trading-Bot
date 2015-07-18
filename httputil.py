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

class SteamBotHttp:

    def __init__(self):
        self.host_normal = 'http://steamcommunity.com'
        self.host_https = 'https://steamcommunity.com'
        self.market = '/market'
        #currency=3 == euro
        self.item_price_viewer = '/priceoverview/?currency=3&appid=730&market_hash_name='
        self.recent_listed = '/recent/?country=PT&language=english&currency=3'
        self.complete_url_item = self.host_normal+self.market+self.item_price_viewer
        self.complete_url_recent = self.host_normal+self.market+self.recent_listed
        self.sell_item_url = self.host_https+self.market+'/sellitem/'
        self.buy_item_url_without_listingid = self.host_https+self.market+'/buylisting/'
        self.render_item_url_first_part = self.host_normal+self.market+'/listings/730/'
        self.render_item_url_sencond_part = '/render/?currency=3'
        self.recent_compare = {}
        self.sessionid = "5cfbd35e404358ce92d5aaa0"
        self.headers_recent_anditem = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cookie':'__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid=5cfbd35e404358ce92d5aaa0; '
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Pragma':'no-cache',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
        }
        self.headers_item_list_ind = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            'Cache-Control':'no-cache',
            'Connection':'keep-alive',
            'Cookie':'__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid=5cfbd35e404358ce92d5aaa0; '
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Pragma':'no-cache',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'
        }
        self.headers_sell = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            "Host": "steamcommunity.com",
            'Cookie': 'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; '
                      '__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                      '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                      'Steam_Language=english; '
                      '730_17workshopQueueTime=1432014476; '
                      'steamRememberLogin=76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba; '
                      'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                      'sessionid=5cfbd35e404358ce92d5aaa0; '
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                      'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                      'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                      'steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170; '
                      'strInventoryLastContext=730_2; '
                      'tsTradeOffersLastRead=1434610877; '
                      'timezoneOffset=3600,0',
            "Referer": "https://steamcommunity.com/id/craked5/inventory",
            "Origin": "https://steamcommunity.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest"
        }
        self.headers_buy = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
            'Connection': 'keep-alive',
            'Content-Length': '83',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; '
                      '__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                      '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                      'Steam_Language=english; '
                      '730_17workshopQueueTime=1432014476; '
                      'steamRememberLogin=76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba; '
                      'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                      'sessionid=5cfbd35e404358ce92d5aaa0; '
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                      'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                      'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                      'steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170; '
                      'strInventoryLastContext=730_2; '
                      'tsTradeOffersLastRead=1434610877; '
                      'timezoneOffset=3600,0',
            'CSP':'active',
            'DNT':'1',
            'Host':'steamcommunity.com',
            'Origin':'http://steamcommunity.com',
            'Referer':'http://steamcommunity.com/market/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
        }
        self.rsa_headers = {
            'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
            'Connection':'keep-alive',
            'Content-Length':44,
            'Content-type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie':'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; '
                     '__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid=5cfbd35e404358ce92d5aaa0; '
                     'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                     'strInventoryLastContext=730_2; '
                     'timezoneOffset=3600,0',
            'CSP':'active',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Origin':'https://steamcommunity.com',
            'Referer':'https://steamcommunity.com/login/home/?goto=0',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
            'X-Prototype-Version':1.7,
            'X-Requested-With':'XMLHttpRequest'
        }
        self.transfer_headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Length':184,
            'Content-Type':'application/x-www-form-urlencoded',
            'Cookie':'browserid=740048883567382728; '
                     'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; '
                     '__utma=128748750.2096343856.1422402525.1426615286.1426972563.6; '
                     '__utmz=128748750.1426972563.6.5.utmcsr=etterstudio.com|utmccn=(referral)|utmcmd=referral|utmcct=/en/pnp.php; '
                     'dp_user_userid=10011565; '
                     'dp_user_password=aEjiUkC3; '
                     'lastagecheckage=1-January-1981; '
                     'recentapps=%7B%22362890%22%3A1430846718%2C%22295110%22%3A1430761022%2C%22252490%22%3A1430173804%2C%22271590%22%3A1428971636%2C%22290930%22%3A1427354378%2C%22353560%22%3A1426972561%2C%22262390%22%3A1424562332%2C%22239140%22%3A1422402521%7D; '
                     'timezoneOffset=3600,0; '
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'steamRememberLogin=76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba; '
                     'dp_user_sessionid=8b4e6fb7c1b244f4330561fa7d87ca7d; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Origin':'https://steamcommunity.com',
            'Referer':'https://steamcommunity.com/login/home/?goto=0',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
        }
        self.headers_logout = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
            'Cache-Control':'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '34',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; '
                      '__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                      '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                      'Steam_Language=english; '
                      '730_17workshopQueueTime=1432014476; '
                      'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                      'sessionid=5cfbd35e404358ce92d5aaa0; '
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                      'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                      'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                      'steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170; '
                      'strInventoryLastContext=730_2; '
                      'tsTradeOffersLastRead=1434610877; '
                      'timezoneOffset=3600,0',
            'DNT':'1',
            'Host':'steamcommunity.com',
            'Origin':'http://steamcommunity.com',
            'Referer':'http://steamcommunity.com/market/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
        }
        self.logout_data = {
            'sessionid' : self.sessionid
        }
        #price = preco que eu quero receber = price+fee_price
        self.data_sell = {
            "sessionid" : self.sessionid,
            "appid" : 730,
            "contextid" : 2,
            "assetid" : 2624120824,
            "amount" : 1,
            "price" : 1000
        }
        #subtotal = price without fee
        #fee = a fee
        #total = price com a fee
        self.data_buy = {
            'sessionid': self.sessionid,
            'currency': 3,
            'subtotal': 0,
            'fee': 0,
            'total': 0,
            'quantity': 1
        }
        self.password = 'Steamgresso1234567@'
        self.rsa_data = {
            'username': 'freeman777',
            'donotcache': 0
        }
        self.login_data = {
            'password':'',
            'username':'freeman777',
            'twofactorcode':'',
            'emailauth':'',
            'loginfriendlyname':'',
            'captchagid':-1,
            'captcha_text':'',
            'emailsteamid':'',
            'rsatimestamp': '',
            'remember_login':'true',
            'donotcache': 0
        }
        self.transfer_data = {
            'steamid': 0,
            'token':'',
            'auth':'',
            'remember_login':'',
            'token_secure':''
        }

    def login(self):
        donotcache = self.now_milliseconds()
        self.rsa_data['donotcache'] = donotcache
        self.login_data['donotcache'] = donotcache
        temp_rsa = req.post('https://steamcommunity.com/login/getrsakey/', headers=self.rsa_headers, data=self.rsa_data)
        print temp_rsa.content
        print 'O status code do GETRSA foi ' + str(temp_rsa.status_code)
        temp_ras_good = ujson.loads(temp_rsa.content)
        self.login_data['rsatimestamp'] = temp_ras_good['timestamp']
        mod = long(temp_ras_good['publickey_mod'], 16)
        exp = long(temp_ras_good['publickey_exp'], 16)
        rsa_key = RSA.construct((mod, exp))
        rsa = PKCS1_v1_5.PKCS115_Cipher(rsa_key)
        encrypted_password = rsa.encrypt(self.password)
        encrypted_password = base64.b64encode(encrypted_password)
        self.login_data['password'] = encrypted_password
        temp_dologin = req.post('https://steamcommunity.com/login/dologin/', headers=self.rsa_headers, data=self.login_data)
        print temp_dologin.content
        print 'O status code do DOLOGIN foi ' + str(temp_dologin.status_code)
        temp_dologin_good = ujson.loads(temp_dologin.content)
        self.transfer_data['steamid'] = temp_dologin_good['transfer_parameters']['steamid']
        self.transfer_data['token'] = temp_dologin_good['transfer_parameters']['token']
        self.transfer_data['auth'] = temp_dologin_good['transfer_parameters']['auth']
        self.transfer_data['remember_login'] = temp_dologin_good['transfer_parameters']['remember_login']
        self.transfer_data['token_secure'] = temp_dologin_good['transfer_parameters']['token_secure']
        temp_transfer = req.post('https://store.steampowered.com/login/transfer', headers=self.transfer_headers,data=self.transfer_data)
        print 'O status code do LOGINTRANSFER foi ' + str(temp_transfer.status_code)

    def logout(self):
        temp_logout = req.post('https://steamcommunity.com/login/logout/', headers= self.headers_logout, data= self.logout_data)
        print 'O status code do LOGOUT FOR ' + str(temp_logout.status_code)


    def now_milliseconds(self):
        self.donotcache = int(time.time() * 1000)

    def urlQueryItem(self,item):
        steam_response = req.get(self.complete_url_item + item,headers=self.headers_recent_anditem)
        try:
            item_temp = ujson.loads(steam_response.text)
        except ValueError:
            return steam_response.status_code, steam_response.text
        #item_temp = decode_dict(item_temp)
        return item_temp
    '''
    def urlQueryRecent(self):
        try:
            steam_response = req.get(self.complete_url_recent,headers=self.headers_recent)
            if steam_response.status_code == 200:
                timestamp = time.time()
                time_temp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))
                self.headers_recent['If-Modified-Since'] = time_temp
                try:
                    recent_temp = ujson.loads(steam_response.text)
                except ValueError:
                    return False
                return recent_temp
            elif steam_response.status_code == 304:
                return -1
        except req.ConnectionError:
            return False
    '''
    def urlQueryRecent(self):
        try:
            steam_response = req.get(self.complete_url_recent, headers=self.headers_recent_anditem)
            print steam_response.status_code
            if steam_response.status_code == 439:
                return False
            else:
                try:
                    recent_temp = ujson.loads(steam_response.text)
                except ValueError:
                    return False
                return recent_temp
        except req.ConnectionError:
            return False

    def urlqueryspecificitemind(self,item):
        try:
            steam_response = req.get(self.render_item_url_first_part+item+self.render_item_url_sencond_part,
                                     self.headers_item_list_ind)
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

    #price = ao preco que eu quero receber
    #price vem em float
    def sellitem(self,assetid,price):
        list_return = []
        price_temp = price * 100
        price_temp = (0.90*price_temp)
        price_temp = round(price_temp)
        self.data_sell['assetid'] = int(assetid)
        self.data_sell['price'] = int(price_temp)
        temp = req.post(self.sell_item_url, data=self.data_sell, headers=self.headers_sell)
        list_return.append(temp.status_code)
        list_return.append(temp.content)
        list_return.append(int(price_temp))
        return list_return

    def buyitem(self,listing,subtotal,fee,currency):
        temp_tuple = []
        self.data_buy['currency'] = int(currency) - 2000
        self.data_buy['subtotal'] = int(subtotal)
        self.data_buy['fee'] = int(fee)
        self.data_buy['total'] = int(self.data_buy['subtotal'] + self.data_buy['fee'])
        temp = req.post(self.buy_item_url_without_listingid+listing, data=self.data_buy, headers=self.headers_buy)
        temp_tuple.append(int(temp.status_code))
        temp_tuple.append(ast.literal_eval(temp.content))
        print temp.status_code
        print temp.content
        return temp_tuple


