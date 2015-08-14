__author__ = 'nunosilva'

import requests
from bs4 import BeautifulSoup
import lxml
import time


i = 0

#temp = requests.get('http://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Doppler%20%28Factory%20New%29')

#soup = BeautifulSoup(temp.text,'html.parser')
#print soup

#print soup.find_all('div',{'class':'pagecontent no_header'})

def trystuff():
    status = 0
    i=0
    while i < 100:
        if status == 0:
            temp = requests.get('http://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Urban%20DDPAT%20(Field-Tested)')
            print 'html ' + str(temp.status_code)
            status = 1
            i +=1
            time.sleep(0.5)

        elif status == 1:
            temp = requests.get('http://steamcommunity.com/market/listings/730/Tec-9%20%7C%20Urban%20DDPAT%20(Field-Tested)/render/?currency=3&start=134')
            print 'render ' + str(temp.status_code)
            status = 0
            i+=1
            time.sleep(0.5)
trystuff()