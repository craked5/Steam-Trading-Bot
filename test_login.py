__author__ = 'nunosilva'

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import requests
import ujson
import time, datetime

def now_milliseconds():
   return int(time.time() * 1000)


# reference: time.mktime() will
# Convert a time tuple in local time to seconds since the Epoch.
password = 'Steamgresso1234567@'
donot = now_milliseconds()
rsa_data = {
    'username': 'freeman777',
    'donotcache': donot
}

rsa_headers = {
    'Accept':'text/javascript, text/html, application/xml, text/xml, */*',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
    'Connection':'keep-alive',
    'Content-Length':44,
    'Content-type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie':'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; __utma=268881843.1944006538.1426348260.1426845397.1427022271.24; __utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Steam_Language=english; 730_17workshopQueueTime=1432014476; recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; sessionid=5cfbd35e404358ce92d5aaa0; steamCountry=PT%7C90d987902b02ceec924245352748dc71; strInventoryLastContext=730_2; timezoneOffset=3600,0',
    'CSP':'active',
    'DNT':1,
    'Host':'steamcommunity.com',
    'Origin':'https://steamcommunity.com',
    'Referer':'https://steamcommunity.com/login/home/?goto=0',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'X-Prototype-Version':1.7,
    'X-Requested-With':'XMLHttpRequest'
}


temp_rsa = requests.post('https://steamcommunity.com/login/getrsakey/', headers=rsa_headers, data=rsa_data)
print temp_rsa.content
temp_ras_good = ujson.loads(temp_rsa.content)


mod = long(temp_ras_good['publickey_mod'], 16)
exp = long(temp_ras_good['publickey_exp'], 16)
rsa_key = RSA.construct((mod, exp))
rsa = PKCS1_v1_5.PKCS115_Cipher(rsa_key)
encrypted_password = rsa.encrypt(password)
encrypted_password = base64.b64encode(encrypted_password)

login_data = {
    'password':encrypted_password,
    'username':'freeman777',
    'twofactorcode':'',
    'emailauth':'',
    'loginfriendlyname':'',
    'captchagid':-1,
    'captcha_text':'',
    'emailsteamid':'',
    'rsatimestamp': temp_ras_good['timestamp'],
    'remember_login':'true',
    'donotcache': donot
}

print encrypted_password

temp_dologin = requests.post('https://steamcommunity.com/login/dologin/', headers=rsa_headers, data=login_data)

print temp_dologin.content
print temp_dologin.status_code