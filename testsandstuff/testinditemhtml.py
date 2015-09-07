__author__ = 'nunosilva'

import requests
from bs4 import BeautifulSoup
import lxml
import time
import random
import ujson


#i = 0

#temp = requests.get('http://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Doppler%20%28Factory%20New%29')

#soup = BeautifulSoup(temp.text,'html.parser')
#print soup

#print soup.find_all('div',{'class':'pagecontent no_header'})
'''
def trystuff():
    list = ['portuguese','english','danish','spanish','russian','chinese','swedish']
    f_items_pobre = open('util/items_pobre50.txt', 'r')
    list_items_to_buy = [line.rstrip('\n') for line in f_items_pobre]
    status = 0
    i=0
    while i < 100:
        current_lang = random.choice(list)
        if status == 0:
            temp = requests.get('http://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Field-Tested%29/render/?query=&start=0&count=1&country=DK&language='+current_lang+'&currency=1')
            print 'html ' + str(temp.status_code)
            print current_lang
            status = 1
            i +=1
            time.sleep(0.2)
        elif status == 1:
            temp = requests.get('http://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Field-Tested%29/render/?query=&start=0&count=1&country=DK&language='+current_lang+'&currency=1')
            print 'render ' + str(temp.status_code)
            print current_lang
            status = 0
            i+=1
            time.sleep(0.2)
'''

'''
def beattradebot():
    list_to_dump = []
    f_items_pobre = open('/Users/nunosilva/util/items_pobre50.txt', 'r')
    list_items_to_buy = [line.rstrip('\n') for line in f_items_pobre]

    for item in list_items_to_buy:
        temp = requests.get('http://steamcommunity.com/market/priceoverview/?currency=3&appid=730&market_hash_name='+item, timeout=10)

        if temp.status_code == 200:
            try:
                temp_content = temp.content.decode('unicode_escape').encode('ascii','ignore')
                temp_content =  ujson.loads(temp_content)
            except:
                print 'Erro'

            if temp_content.has_key('median_price'):
                try:
                    lowest_price = temp_content['lowest_price']
                    print lowest_price
                    lowest_price = lowest_price.decode('unicode_escape').encode('ascii','ignore')
                    lowest_price = lowest_price.replace(',','.').replace('-','0')

                    median_price = temp_content['median_price']
                    median_price = median_price.decode('unicode_escape').encode('ascii','ignore')
                    median_price = median_price.replace(',','.').replace('-','0')

                    list_to_dump.append("O " + item + " tem preco medio " + str(median_price) + ' e preco baixo ' + str(lowest_price) + '\n')
                except (ValueError,KeyError):
                    print "key error no item " + item
            else:
                print "erro no item " + item

    file1 = open('/Users/nunosilva/util/itemtest.txt','a')
    for item in list_to_dump:
        file1.write(item)

beattradebot()
'''

