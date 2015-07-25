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
transfer_headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':184,
    'Content-Type':'application/x-www-form-urlencoded',
    'Cookie':'browserid=740048883567382728; steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; __utma=128748750.2096343856.1422402525.1426615286.1426972563.6; __utmz=128748750.1426972563.6.5.utmcsr=etterstudio.com|utmccn=(referral)|utmcmd=referral|utmcct=/en/pnp.php; dp_user_userid=10011565; dp_user_password=aEjiUkC3; lastagecheckage=1-January-1981; recentapps=%7B%22362890%22%3A1430846718%2C%22295110%22%3A1430761022%2C%22252490%22%3A1430173804%2C%22271590%22%3A1428971636%2C%22290930%22%3A1427354378%2C%22353560%22%3A1426972561%2C%22262390%22%3A1424562332%2C%22239140%22%3A1422402521%7D; timezoneOffset=3600,0; steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; steamRememberLogin=76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba; dp_user_sessionid=8b4e6fb7c1b244f4330561fa7d87ca7d; steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170',
    'DNT':1,
    'Host':'steamcommunity.com',
    'Origin':'https://steamcommunity.com',
    'Referer':'https://steamcommunity.com/login/home/?goto=0',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
}

headers_logout = {
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
logout_data = {
    'sessionid' :'sessionid=5cfbd35e404358ce92d5aaa0 '
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

temp_dologin_good = ujson.loads(temp_dologin.content)
print temp_dologin_good

time.sleep(2)
transfer_data = {
    'steamid': 0,
    'token':'',
    'auth':'',
    'remember_login':'',
    'token_secure':''
}

transfer_data['steamid'] = temp_dologin_good['transfer_parameters']['steamid']
transfer_data['token'] = temp_dologin_good['transfer_parameters']['token']
transfer_data['auth'] = temp_dologin_good['transfer_parameters']['auth']
transfer_data['remember_login'] = temp_dologin_good['transfer_parameters']['remember_login']
transfer_data['token_secure'] = temp_dologin_good['transfer_parameters']['token_secure']

temp_transfer = requests.post('https://store.steampowered.com/login/transfer', headers=transfer_headers,data=transfer_data)
print temp_transfer.content
print temp_transfer.status_code

temp_logout = requests.post('https://steamcommunity.com/login/logout/', headers= headers_logout, data= logout_data)
print temp_logout.content
print temp_logout.status_code

temp_logout_good = ujson.loads(temp_logout.content)

