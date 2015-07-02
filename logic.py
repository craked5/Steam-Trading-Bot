#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'
__author__ = 'github.com/craked5'

import os
import decimal
import time
class Logic:

    def __init__(self,mode):
        if mode == 'recent':
            try:
                self.f = open('items_pobre.txt', 'r')
            except IOError:
                print "Error opening the list file"
            print "file was opened ok"
            #primeira leitura do ficheiro
            self.list_items_to_buy = [line.rstrip('\n') for line in self.f]
            self.wallet_balance = 0
            self.f.close()
            try:
                self.f2 = open('wallet.txt', 'r')
            except IOError:
                print "Error opening the list file"
            print "file was opened ok"
            self.wallet_balance = self.f2.readlines()
            self.wallet_balance = float(self.wallet_balance[0])
            self.f2.close()
            print self.wallet_balance
        elif mode == 'item':
            self.wallet_balance = 0
            try:
                self.f2 = open('wallet.txt', 'r')
            except IOError:
                print "Error opening the list file"
            print "file was opened ok"
            self.wallet_balance = self.f2.readlines()
            self.wallet_balance = float(self.wallet_balance[0])
            self.f2.close()
            print self.wallet_balance

    def writeInItemsTxt(self,item):
        try:
            tempfile = open('items_pobre.txt', 'a')
            tempfile.write(item+'\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        except IOError:
            print "Erro ao escrever no ficheiro"
            return False
        tempfile2 = open('items_pobre.txt', 'r')
        self.list_items_to_buy = [line.rstrip('\n') for line in tempfile2]
        tempfile2.close()
        print 'New List: '
        print self.list_items_to_buy
        print item + " was added to the list!"
        return True

    def delInItemsTxt(self,item):
        tempfile = open('items_pobre.txt', 'r')
        lines = [line1.rstrip('\n') for line1 in tempfile]
        print lines
        tempfile.close()
        try:
            tempfile2 = open('items_pobre.txt', 'w')
            for line2 in lines:
                if line2.rstrip('\n')!=item:
                    tempfile2.write(line2+'\n')
                    tempfile2.flush()
                    os.fsync(tempfile2.fileno())
            tempfile2.close()
            tempfile3 = open('items_pobre.txt', 'r')
            self.list_items_to_buy = [line3.rstrip('\n') for line3 in tempfile3]
            tempfile3.close()
        except IOError:
            print 'Error deleting item, try again please'
            return False
        print item + ' was removed from the list! YAY'
        print 'New List: '
        print self.list_items_to_buy
        return True

    #balance - int
    def writetowallet(self,balance):
        temp = decimal.Decimal(balance) / 100
        wallet_balance = float(temp)
        wallet_balance = str(wallet_balance)
        try:
            tempfile = open('wallet.txt','w')
            tempfile.write(wallet_balance)
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
            self.wallet_balance = wallet_balance
        except IOError:
            print "Error doing stuff"
            return False
        except TypeError:
            print "erro ao escrever stuff na wallet"
            return False
        return True


    def writetobuys(self,subtotal,fee,data_buy,listingid,key,responsecode,responsedict):
        tempfile = open('buys.txt', 'a')
        temp_string2 = 'A data buy foi ' + str(data_buy)
        temp_string3 = 'A codigo de resposta foi ' + str(responsecode) + ' e o dict de resposta foi ' + str(responsedict)
        temp_string4 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")
        if responsecode == 502:
            temp_string = 'Tentei comprar ' + key + ' com a listingid ' + str(listingid) + ' ao preco de ' + str(subtotal+fee)
            tempfile.write(temp_string+'\n')
            tempfile.write(temp_string2+'\n')
            tempfile.write(temp_string3+'\n')
            tempfile.write(temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        elif responsecode == 200:
            temp_string = 'Comprei ' + key + ' com a listingid ' + str(listingid) + ' ao preco de ' + str(subtotal+fee)
            tempfile.write(temp_string+'\n')
            tempfile.write(temp_string2+'\n')
            tempfile.write(temp_string3+'\n')
            tempfile.write(temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()

    def writetosells(self,status,content,item,price,balance):
        tempfile = open('sells.txt','a')
        if status == 502:
            temp_string = 'Tentei vender a ' + item + ' ao preco ' + str(price) + ' mas o codigo foi ' + str(status)
            temp_string2 = 'O content foi: ' + content
            temp_string3 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")
            temp_string4 = 'O balance depois da sale ficara ' + str(balance)
            tempfile.write(temp_string+'\n')
            tempfile.write(temp_string2+'\n')
            tempfile.write(temp_string3+'\n')
            tempfile.write(temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        elif status == 200:
            temp_string = 'Vendi a ' + item + ' ao preco ' + str(price) + ' e o codigo foi ' + str(status)
            temp_string2 = 'O content foi: ' + content
            temp_string3 = 'HORA: ' + time.strftime("%H:%M:%S") + ' e DATA: ' + time.strftime("%d/%m/%Y")
            temp_string4 = 'O balance depois da sale ficara ' + str(balance)
            tempfile.write(temp_string+'\n')
            tempfile.write(temp_string2+'\n')
            tempfile.write(temp_string3+'\n')
            tempfile.write(temp_string4+'\n\n\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()

    def writetoerrors(self,error,content):
        pass