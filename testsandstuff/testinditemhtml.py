__author__ = 'nunosilva'

import requests
from bs4 import BeautifulSoup
import lxml


i = 0

temp = requests.get('http://steamcommunity.com/market/listings/730/%E2%98%85%20Bayonet%20%7C%20Doppler%20%28Factory%20New%29')

soup = BeautifulSoup(temp.text,'html.parser')
print soup

print soup.find_all('div',{'class':'pagecontent no_header'})
