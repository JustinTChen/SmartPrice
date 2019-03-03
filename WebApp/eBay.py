from urllib.request import urlopen
import json
import requests

import matplotlib
from datascience import *
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('fivethirtyeight')
sns.set()
sns.set_context("talk")

##############################################################################
"*** RETURNS CATEGORY ID FROM USER CATEGORY INPUT ***"
##############################################################################
def findID(category):
    cats = Table().read_table("categories.csv")
    return cats.where('Category', category).column('#').item(0)

##############################################################################
"*** RETURNS Condition Integer FROM USER Condition String ***"
##############################################################################
def findCondition(condition):
    if condition == "New":
        return 1000
    return 3000

def calculate(search_term, category, condition):
    ##########################################################################
    "*** API ***"
    ##########################################################################
    key = 'JustinCh-SmartPri-PRD-416e5579d-aa266db1'
    keywords = search_term.replace(' ', '+')
    category = findID(category)
    condition = findCondition(condition)
    url = ("http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findCompletedItems&SERVICE-VERSION=1.7.0&SECURITY-APPNAME=JustinCh-SmartPri-PRD-416e5579d-aa266db1&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&keywords=" + keywords + "&categoryId=" + str(category) + "&itemFilter(0).name=Condition&itemFilter(0).value=" + str(condition) + "&itemFilter(1).name=FreeShippingOnly&itemFilter(1).value=false&itemFilter(2).name=SoldItemsOnly&itemFilter(2).value=true")

    ###########################################################################
    "*** CLEANS UP .JSON TO PANDAS DATAFRAME ***"
    ###########################################################################
    apiResult = requests.get(url)
    listings, prices, offer, BIN = [], [], [], []
    parsed = apiResult.json()
    numPages = int(parsed["findCompletedItemsResponse"][0]['paginationOutput'][0]['totalPages'][0])
    if numPages > 10:
        numPages = 10
    for page in range(1, numPages+1):
        apiResult_page = requests.get(url+"&paginationInput.pageNumber=" + str(page))
        parsed_page = apiResult_page.json()
        for item in parsed_page["findCompletedItemsResponse"][0]["searchResult"][0]["item"]:
            listings.append(item['title'][0])
            prices.append(float(item['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__']))
            offer.append(item['listingInfo'][0]['bestOfferEnabled'][0])
            BIN.append(item['listingInfo'][0]['buyItNowAvailable'][0])
    ###########################################################################
    "*** PANDAS OPERATIONS FROM TABLE TO GRAPH ***"
    ###########################################################################
    dataTable = pd.concat([pd.Series(listings), pd.Series(prices), pd.Series(offer), pd.Series(BIN)], axis=1)
    dataTable.columns = ['Name', 'Price', 'Best Offer Enabled', "Buy It Now"]
    dataTable

    plt.figure(figsize=(8, 6))
    lowLimit = np.percentile(np.array(dataTable['Price']), 2.5)
    highLimit = np.percentile(np.array(dataTable['Price']), 97.5)
    sns.distplot(dataTable['Price'],rug=True, norm_hist=True, color='teal')
    plt.ylabel('Proportion of Sales')
    plt.xlim(lowLimit, highLimit)
    plt.title('Price Distribution for ' + search_term + ' Sold');
    plt.savefig('dist.png')

    stats = dataTable.describe()['Price']
    summary = ["$" + str(round(x, 2)) for x in [stats[1], stats[2], stats[4], stats[5], stats[6]]]

    from io import BytesIO
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)  # rewind to beginning of file
    import base64
    graph = base64.b64encode(open('dist.png', 'rb').read()).decode('utf-8').replace('\n', '')
    ###########################################################################
    "*** RETURN DICT OF IMPORTANT INFO ***"
    ###########################################################################
    low, high = round(min(stats[1], stats[5]), 2), round(max(stats[1], stats[5]), 2)
    return {'Mean':summary[0], 'SD':summary[1], '25%':summary[2], '50%':summary[3], '75%':summary[4], 'Min':"$"+str(low), 'Max':"$"+str(high), 'Graph':graph}
