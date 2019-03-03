from urllib.request import urlopen
import json
import requests

from datascience import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

###############################################################################
"*** API KEY ***"
##############################################################################
key = 'JustinCh-SmartPri-PRD-416e5579d-aa266db1'

###############################################################################
"*** RETURNS CATEGORY ID FROM USER CATEGORY INPUT ***"
##############################################################################
def findID(category):
    cats = Table().read_table("categories.csv")
    return cats.where('Category', category).column('#').item(0)

###############################################################################
"*** USER INPUT ***"
##############################################################################
search_term = "air+jordan+1" #user_input.reaplce(" ","+")
category = 11450 #findID(categoryInput) #11450
#New or Used (1000 or 3000)
condition = 1000 #NEW

###############################################################################
"*** eBay API CALL ***"
##############################################################################
url = ("http://svcs.ebay.com/services/search/FindingService/v1?\
        OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0\
        &SECURITY-APPNAME=JustinCh-SmartPri-PRD-416e5579d-aa266db1&\
        RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD\
        &keywords=" + search_term + "&categoryId=" + str(category) + "\
        &itemFilter(0).name=Condition\
        &itemFilter(0).value=" + str(condition) + "\
        &itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=false\
        &itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true")

###############################################################################
"*** CLEANS UP .JSON TO PANDAS DATAFRAME ***"
##############################################################################
listings, prices, offer, BIN = [], [], [], []
apiResult = requests.get(url)
parsed = apiResult.json()
items_dict = parsed["findCompletedItemsResponse"][0]["searchResult"][0]["item"]
for item in items_dict:
    listings.append(item['title'][0])
    prices.append(item['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__'])
    offer.append(item['listingInfo'][0]['bestOfferEnabled'])
    BIN.append(item['listingInfo'][0]['buyItNowAvailable'])

dataTable = pd.concat([pd.Series(listings), pd.Series(prices), pd.Series(offer), pd.Series(BIN)], axis=1)
dataTable.columns = ['Name', 'Price', 'Best Offer Enabled', "Buy It Now"]

"""
http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0
&SECURITY-APPNAME=JustinCh-SmartPri-PRD-416e5579d-aa266db1&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=air+jordan+1
&categoryId=11450&itemFilter(0).name=Condition&itemFilter(0).value=3000&itemFilter(1).name=FreeShippingOnly
&itemFilter(1).value=true&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true&sortOrder=PricePlusShippingLowest


&paginationInput.entriesPerPage=2
"http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0\
&SECURITY-APPNAME=JustinCh-SmartPri-PRD-416e5579d-aa266db1&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD\
&keywords=" + search_term + "&categoryId=" + str(category) + "&itemFilter(0).name=Condition\
&itemFilter(0).value=" + str(condition) + "&itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=false\
&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true&sortOrder=PricePlusShippingLowest&paginationInput.entriesPerPage=2"

"""
