#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'nunosilva'

import json
import yaml

class SteamJson:

    def __init__(self):
        self.first_parsing_list = ['results_html','hovers','last_listing','last_time','app_data','currency',
                                    'success','more','purchaseinfo']
        self.asset_parsing_list = ['currency','contextid','classid','instanceid','amount','status','original_amount',
                                   'background_color','icon_url','icon_large_url','descriptions', '0','name','name_color','type','market_name','market_actions',
                                              'commodity','app_icon','owner']
        self.listinginfo_parsing_list = []
        self.asset_list = None
        self.clean_assets = None
        self.listinginfo_list = None
        self.clean_listings = None
        self.recent_parsed = None


    def getRecentTotalReady(self, recent_full):
        for key in self.first_parsing_list:
           self.recent_parsed = recent_full.pop[key,None]
        #retorna um dict so com as keys assets e listinginfo
        return self.recent_parsed


    def getCleanAssetList(self):
        self.asset_list = self.recent_parsed['assets']
        self.asset_list = self.asset_list['730']
        self.asset_list = self.asset_list['2']
        for key in self.asset_parsing_list:
            self.asset_list = self.asset_list.pop(key,None)

