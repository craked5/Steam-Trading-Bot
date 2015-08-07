__author__ = 'nunosilva, github.com/craked5'

class Httpheaders:

    def __init__(self):
        self.sessionid = "701e95194399b26e87b16329"

        self.headers_wallet = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            'Connection':'keep-alive',
            'Cookie':'__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days'
                     '%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A'
                     '0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'HTTPS':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36'
        }

        self.headers_active_listings = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            'Connection':'keep-alive',
            'Cookie':'__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days'
                     '%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A'
                     '0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Referer':'http://steamcommunity.com/market/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36',
            'X-Requested-With':'XMLHttpRequest'
        }

        self.headers_item_priceoverview = {
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
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days'
                     '%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A'
                     '0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36'
        }

        self.headers_recent = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "pt-PT,pt;q=0.8,en-US;q=0.6,en;q=0.4,fr;q=0.2,es;q=0.2",
            'Connection':'keep-alive',
            'Cache-Control':'max-age=0',
            'Cookie':'__utma=268881843.1944006538.1426348260.1426845397.1427022271.24; '
                     '__utmz=268881843.1427022271.24.22.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); '
                     'Steam_Language=english; '
                     '730_17workshopQueueTime=1432014476; '
                     'recentlyVisitedAppHubs=220%2C316950%2C440%2C72850%2C295110%2C730; '
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days'
                     '%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A'
                     '0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'If-Modified-Since':'Sat, 18 Jul 2015 22:48:42 GMT',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36'
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
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7Ceadce223f9093afc9f086e613abc8402; '
                     'strInventoryLastContext=730_2; '
                     'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                     'timezoneOffset=3600,0; '
                     'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days'
                     '%22%3A15%2C%22sales_this_year%22%3A133%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%3A'
                     '0%2C%22new_device_cooldown_days%22%3A7%7D; '
                     'tsTradeOffersLastRead=1435052082',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Upgrade-Insecure-Requests':1,
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36'
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
                      'sessionid='+self.sessionid+';'
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_day'
                      's%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%'
                      '3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
                      'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                      'steamLogin=76561197979199766%7C%7C9E4F945373E086AE0ABD1A71CEEC718241E2E2B2; '
                      'steamLoginSecure=76561197979199766%7C%7CEEF7B52C4A0259FBA5D09A596F0CE2484EAE7170; '
                      'strInventoryLastContext=730_2; '
                      'tsTradeOffersLastRead=1434610877; '
                      'timezoneOffset=3600,0',
            "Referer": "https://steamcommunity.com/id/craked5/inventory",
            "Origin": "https://steamcommunity.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/43.0.2357.124 Safari/537.36",
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
                      'sessionid='+self.sessionid+';'
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_day'
                      's%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%'
                      '3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
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
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.124 Safari/537.36'
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
                     'sessionid='+self.sessionid+';'
                     'steamCountry=PT%7C90d987902b02ceec924245352748dc71; '
                     'strInventoryLastContext=730_2; '
                     'timezoneOffset=3600,0',
            'CSP':'active',
            'DNT':1,
            'Host':'steamcommunity.com',
            'Origin':'https://steamcommunity.com',
            'Referer':'https://steamcommunity.com/login/home/?goto=0',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.130 Safari/537.36',
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
                     'recentapps=%7B%22362890%22%3A1430846718%2C%22295110%22%3A1430761022%2C%22252490%22%3A1430173804%2C'
                     '%22271590%22%3A1428971636%2C%22290930%22%3A1427354378%2C%22353560%22%3A1426972561%2C%22262390%22%3'
                     'A1424562332%2C%22239140%22%3A1422402521%7D; '
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
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
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
                      'sessionid='+self.sessionid+';'
                      'webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_day'
                      's%22%3A15%2C%22sales_this_year%22%3A101%2C%22max_sales_per_year%22%3A200%2C%22forms_requested%22%'
                      '3A0%2C%22new_device_cooldown_days%22%3A7%7D; '
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
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/43.0.2357.124 Safari/537.36'
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

