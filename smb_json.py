#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import json
import yaml

class SteamJson:

    def __init__(self):
        self.first_parsing_list = [u'results_html',u'hovers',u'last_listing',u'last_time',u'app_data',u'currency',
                                    u'success',u'more',u'purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount','status','original_amount',
                                   'background_color','icon_url','icon_url_large','descriptions','name','name_color','type','market_name','market_actions',
                                              'commodity','app_icon','owner','actions']
        self.listinginfo_parsing_list = []
        self.clean_assets = None
        self.listinginfo_list = None
        self.clean_listings = None


    def getRecentTotalReady(self, recent_full):
        for key in self.first_parsing_list:
            print key
            recent_full.pop(key)
        #retorna um dict so com as keys assets e listinginfo
        self.recent_parsed = recent_full
        print self.recent_parsed
        return self.recent_parsed


    def getCleanAssetList(self):
        self.asset_list = self.recent_parsed['assets']
        self.asset_list = self.asset_list['730']
        self.asset_list = self.asset_list['2']
        print self.asset_list
        for key_item in self.asset_list:
            for key in self.asset_parsing_list:
                self.asset_list[key_item].pop(key)
        self.clean_assets = self.asset_list
        return self.clean_assets

