#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva, github.com/craked5'


import os
import decimal
import time
from random import shuffle
class Logic:

    def __init__(self,mode,ind_hosts,dif_countries,items_list):
        self.list_hosts = []
        self.ids_active_listings = []

        if mode == 'recent':

            self.wallet_balance = 0
            host_mode = raw_input('Quer mudar as hosts de cada querie no modo RECENT LISTINGS (n/y)? \n')

            if host_mode == 'y':
                self.dif_hosts_recent='yes'
                what_hosts = raw_input('Qual as hosts que pretende (eu/us1/us2/useu/asia/world)? \n')

                f_hosts = open('util/hosts_'+what_hosts+'.txt','r')
                self.list_hosts = [line.rstrip('\n') for line in f_hosts]
                shuffle(self.list_hosts)
                print self.list_hosts

            elif host_mode == 'n':
                self.dif_hosts_recent = 'no'

            dif_countries = raw_input('Quer mudar os country code do RECENT (n/y)? \n')
            if dif_countries == 'y':
                self.dif_countries = 'yes'
                try:
                    f_list_countries = open('util/list_countries.txt', 'r')
                    self.list_countries = [line.rstrip('\n') for line in f_list_countries]
                    print "ITEMS TO BUY file was opened ok"
                    f_list_countries.close()
                except IOError:
                    print "Error opening the items to buy list file!"
            else:
                self.dif_countries = 'no'

            try:
                f_items_pobre = open('util/'+items_list+'.txt', 'r')
                self.list_items_to_buy = [line.rstrip('\n') for line in f_items_pobre]
                print "ITEMS TO BUY file was opened ok"
                f_items_pobre.close()
            except IOError:
                print "Error opening the items to buy list file!"

            try:
                f_listings = open('util/active_listings.txt','r')
                self.ids_active_listings = [line.rstrip('\n') for line in f_listings]
                print "ACTIVE LISTINGS FILE WAS OPENED OK"
            except IOError:
                print 'Error opening active listings file!'

            try:
                f_wallet = open('util/wallet.txt', 'r')
                self.wallet_balance = f_wallet.readlines()
                self.wallet_balance = float(self.wallet_balance[0])
                print "wallet file file was opened ok"
                f_wallet.close()
            except IOError:
                print "Error opening the wallet file"

            print self.wallet_balance

        elif mode == 'item':

            if dif_countries == 'y':
                try:
                    f_list_countries = open('util/list_countries.txt', 'r')
                    self.list_countries = [line.rstrip('\n') for line in f_list_countries]
                    print "COuntry list file was opened ok"
                    f_list_countries.close()
                except IOError:
                    print "Error opening the items to buy list file!"

            try:
                f_listings = open('util/active_listings.txt','r')
                self.ids_active_listings = [line.rstrip('\n') for line in f_listings]
                print "ACTIVE LISTINGS FILE WAS OPENED OK"
            except IOError:
                print 'Error opening active listings file!'

            self.wallet_balance = 0
            try:
                f_wallet = open('util/wallet.txt', 'r')
                f_hosts = open('util/hosts_'+ind_hosts+'.txt','r')
            except IOError:
                print "Error opening the list file"
            print "wallet and hosts files was opened ok"
            self.list_hosts = [line.rstrip('\n') for line in f_hosts]
            print len(self.list_hosts)
            shuffle(self.list_hosts)
            self.wallet_balance = f_wallet.readlines()
            self.wallet_balance = float(self.wallet_balance[0])
            f_wallet.close()
            f_hosts.close()
            print self.wallet_balance

    def writeInItemsTxt(self,item):

        try:
            tempfile = open('util/items_pobre50.txt', 'a')
            tempfile.write(item+'\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        except IOError:
            print "Erro ao escrever no ficheiro"
            return False

        tempfile2 = open('util/items_pobre50.txt', 'r')
        self.list_items_to_buy = [line.rstrip('\n') for line in tempfile2]
        tempfile2.close()

        print 'New List: '
        print self.list_items_to_buy
        print item + " was added to the list!"

        return True

    def delInItemsTxt(self,item):

        tempfile = open('util/items_pobre50.txt', 'r')
        lines = [line1.rstrip('\n') for line1 in tempfile]
        print lines
        tempfile.close()

        try:
            tempfile2 = open('util/items_pobre50.txt', 'w')
            for line2 in lines:
                if line2.rstrip('\n')!=item:
                    tempfile2.write(line2+'\n')
                    tempfile2.flush()
                    os.fsync(tempfile2.fileno())
            tempfile2.close()
            tempfile3 = open('util/items_pobre50.txt', 'r')
            self.list_items_to_buy = [line3.rstrip('\n') for line3 in tempfile3]
            tempfile3.close()
        except IOError:
            print 'Error deleting item, try again please'
            return False

        print item + ' was removed from the list! YAY'
        print 'New List: '
        print self.list_items_to_buy

        return True

    #escreve para o ficheiro wallet e actualiza a var wallet_balance com o balance
    #balance - int
    def writetowallet(self,balance):

        temp = decimal.Decimal(balance) / 100
        wallet_balance = float(temp)
        wallet_balance = str(wallet_balance)

        try:
            tempfile = open('util/wallet.txt','w')
            tempfile.write(wallet_balance)
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            self.wallet_balance = float(wallet_balance)
        except IOError:
            print "Error doing stuff"
            return False
        except TypeError:
            print "erro ao escrever stuff na wallet"
            return False

        return True

    #escreve para o active_listings.txt e actualiza a var active_listings
    def writetoactivelistings(self,id):

        try:
            tempfile = open('util/active_listings.txt', 'a')
            tempfile.write(id+'\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        except IOError:
            print "Erro ao escrever no ficheiro das active listings"
            return False

        tempfile2 = open('util/active_listings.txt', 'r')
        self.ids_active_listings = [line.rstrip('\n') for line in tempfile2]
        tempfile2.close()

        print 'Current active Listings: '
        print self.ids_active_listings
        print id + " was added to the active listings list!"

        return True

    #delete an id from the active_listings.txt file and updates the active_listings self var
    def deletefromactivelistings(self,id):

        tempfile = open('util/active_listings.txt', 'r')
        lines = [line1.rstrip('\n') for line1 in tempfile]
        print lines
        tempfile.close()

        try:
            tempfile2 = open('util/active_listings.txt', 'w')
            for line2 in lines:
                if line2.rstrip('\n')!=id:
                    tempfile2.write(line2+'\n')
                    tempfile2.flush()
                    os.fsync(tempfile2.fileno())
            tempfile2.close()
            tempfile3 = open('util/active_listings.txt', 'r')
            self.ids_active_listings = [line3.rstrip('\n') for line3 in tempfile3]
            tempfile3.close()
        except IOError:
            print 'Error deleting item, try again please'
            return False

        print id + ' was removed from the active listings list! YAY'
        print 'Currenty active listings selling: '
        print self.ids_active_listings

        return True

    def writenewactivelistings(self,list):
        try:
            f_listings = open('util/active_listings.txt', 'w')
            for id in list:
                f_listings.write(id+'\n')
                f_listings.flush()
                os.fsync(f_listings.fileno())
        except IOError:
            return False
        f_listings.close()
        self.ids_active_listings = list
        return self.ids_active_listings



    def writetobuyfile(self,subtotal,fee,data_buy,listingid,key,responsecode,responsedict,thread_n):

        tempfile = open('util/buys.txt', 'a')
        temp_string2 = 'A data buy foi ' + str(data_buy)
        temp_string3 = 'A codigo de resposta foi ' + str(responsecode) + ' e o dict de resposta foi ' + str(responsedict)
        temp_string4 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")

        if responsecode == 502:
            temp_string = 'A thread ' + str(thread_n) + ' tentou comprar ' + key + ' com a listingid ' + \
                          str(listingid) + ' ao preco de ' + str(subtotal+fee)
            tempfile.write(temp_string+'\n'+temp_string2+'\n'+temp_string3+'\n'+temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            return True

        elif responsecode == 200:
            temp_string = 'A thread ' + str(thread_n) + ' comprou a ' + key + ' com a listingid ' + \
                          str(listingid) + ' ao preco de ' + str(subtotal+fee)
            tempfile.write(temp_string+'\n'+temp_string2+'\n'+temp_string3+'\n'+temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            return True

        else:
            return False

    def writetosellfile(self,status,content,item,price,thread_n,price_no_fee):

        tempfile = open('util/sells.txt','a')

        if status == 502:
            temp_string = 'A thread ' + str(thread_n) + 'Tentou vender a ' + item + ' ao preco ' + str(price) + \
                          ' e eu ia receber '+ str(price_no_fee) + ' mas o codigo foi ' + str(status)
            temp_string2 = 'O content foi: ' + content
            temp_string3 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")
            tempfile.write(temp_string+'\n'+temp_string2+'\n'+temp_string3+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            return True

        elif status == 200:
            temp_string = 'A thread ' + str(thread_n) + ' Vendeu a ' + item + ' ao preco ' + str(price) + \
                          ' e vou receber '+ str(price_no_fee) + ' e o codigo foi ' + str(status)
            temp_string2 = 'O content foi: ' + content
            temp_string3 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")
            tempfile.write(temp_string+'\n'+temp_string2+'\n'+temp_string3+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            return True

        elif status == 'venda':
            pass

        else:
            return False



    def writetofileip(self,ip,thread):

        try:
            tempfile = open('util/fail_ip.txt', 'a')
            tempfile.write('A thread ' + thread +' falhou no ip '+ ip +'\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        except IOError:
            print "Erro ao escrever no ficheiro"
            return False

        return True