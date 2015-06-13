#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import os
from smb_requests_recent import SteamBotHttp

class Logic:

    def __init__(self):
        try:
            self.f = open('items.txt', 'r')
        except IOError:
            print "Error opening the list file"
        print "file was opened ok"
        print self.f
        #primeira leitura do ficheiro
        self.list_items_to_buy = [line.rstrip('\n') for line in self.f]
        self.f.close()
        print self.list_items_to_buy

    def writeInItemsTxt(self,item):
        try:
            tempfile = open('items.txt', 'a')
            tempfile.write(item+'\n')
            tempfile.flush()
            os.fsync(tempfile.fileno())
            tempfile.close()
        except IOError:
            print "Erro ao escrever no ficheiro"
            return False
        tempfile2 = open('items.txt', 'r')
        self.list_items_to_buy = [line.rstrip('\n') for line in tempfile2]
        tempfile2.close()
        print 'New List: '
        print self.list_items_to_buy
        print item + " was added to the list!"
        return True

    def delInItemsTxt(self,item):
        tempfile = open('items.txt', 'r')
        lines = [line1.rstrip('\n') for line1 in tempfile]
        print lines
        tempfile.close()
        try:
            tempfile2 = open('items.txt', 'w')
            for line2 in lines:
                if line2.rstrip('\n')!=item:
                    tempfile2.write(line2+'\n')
                    tempfile2.flush()
                    os.fsync(tempfile2.fileno())
            tempfile2.close()
            tempfile3 = open('items.txt', 'r')
            self.list_items_to_buy = [line3.rstrip('\n') for line3 in tempfile3]
            tempfile3.close()
        except IOError:
            print 'Error deleting item, try again please'
            return False
        print item + ' was removed from the list! YAY'
        print 'New List: '
        print self.list_items_to_buy
        return True

