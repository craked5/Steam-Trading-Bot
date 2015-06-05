#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import os
from smb_requests_recent import SteamBotHttp

class Logic:

    def __init__(self):
        try:
            self.f = open('items.txt', 'a+')
        except IOError:
            print "Error opening the list file"
        #primeira leitura do ficheiro
        self.list_items = [line.rstrip('\n') for line in self.f]

    def writeInItemsTxt(self,item):
        try:
            self.f.write(item)
            self.f.flush()
            os.fsync(self.f.fileno())
        except IOError:
            return False
        self.list_items = [line.rstrip('\n') for line in self.f]
        print 'New List: ' + self.list_items
        print item + " was added to the list!"
        return True

    def delInItemsTxt(self,item):
        self.f.seek(0)
        try:
            for line in self.list_items:
                if line != item:
                    self.f.write(line)
                    self.f.flush()
                    os.fsync(self.f.fileno())
            self.f.truncate()
            self.list_items = [line.rstrip('\n') for line in self.f]
        except IOError:
            print 'Error deleting item, try again please'
            return False
        print item + ' was removed from the list! YAY'
        print 'New List: ' + self.list_items
        return True

