__author__ = 'nunosilva'

import http

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2',
    'Connection': 'keep-alive',
    'Content-Length': '83',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'steamMachineAuth76561197979199766=5682D02C36EBD479EC086107B2EC135E267C9385; __utma=268881843.1944006538.1426348260.1426845397.1427022271.24; __utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); Steam_Language=english; 730_17workshopQueueTime=1432014476; steamRememberLogin=76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba; recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; sessionid=9d8e0a5043cccddd6c430395; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D; steamCountry=PT%7C90d987902b02ceec924245352748dc71; steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170; strInventoryLastContext=730_2; tsTradeOffersLastRead=1434610877; timezoneOffset=3600,0',
    'CSP':'active',
    'DNT':'1',
    'Host':'steamcommunity.com',
    'Origin':'http://steamcommunity.com',
    'Referer':'http://steamcommunity.com/market/listings/730/USP-S%20%7C%20Stainless%20%28Battle-Scarred%29',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124 Safari/537.36'
}

data = {
    'sessionid':'9d8e0a5043cccddd6c430395',
    'currency':3,
    'subtotal':2,
    'fee':2,
    'total':4,
    'quantity':1
}

cookies2 = {
    'steamMachineAuth76561197979199766':'5682D02C36EBD479EC086107B2EC135E267C9385',
    '__utma':'268881843.1944006538.1426348260.1426845397.1427022271.24',
    '__utmz':'268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    'Steam_Language':'english',
    '730_17workshopQueueTime':'1432014476',
    'steamRememberLogin':'76561197979199766%7C%7Cdf433a77e3eee7d7e472716c8ce2dfba',
    'recentlyVisitedAppHubs':'220%2C316950%2C440%2C72850%2C295110%2C730',
    'sessionid':'9d8e0a5043cccddd6c430395',
    'webTradeEligibility':'%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A0%2C%22new_device_cooldown_days%22%3A7%7D',
    'steamCountry':'PT%7C90d987902b02ceec924245352748dc71',
    'steamLogin':'76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2',
    'steamLoginSecure':'76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170',
    'strInventoryLastContext':'730_2',
    'tsTradeOffersLastRead':'1434610877',
    'timezoneOffset':'3600,0'
}

target = 'https://steamcommunity.com/market/buylisting/427059585535864200'

temp =  http.post(target, data=data, headers=headers)
