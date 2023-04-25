import os
import datetime as dt
from datetime import datetime
from datetime import timedelta
import datetime as dt
import requests
import json
from requests_negotiate_sspi import HttpNegotiateAuth
import pandas as pd
import numpy as np
import re
import glob

filelocation=r'C:\\Python\\TextTT_Dash\\fills_folder\\'

def fetchData(date):
    requestURL = "http://hgdataapi/TT/FillsAudit"
    fromDate=date
    toDate=date    #From and to date must be same for only one day can be supplied by API
    

    r = requests.get('{url}?from={fromDate}&to={toDate}'.format(url=requestURL, fromDate=fromDate, toDate=toDate),auth=HttpNegotiateAuth())
    if r.status_code == 200: 
        try:    
            jsonResponse = json.loads(r.text.encode('ascii', 'ignore'))
            df=pd.DataFrame(jsonResponse)
        except: 
            print()
    else:
        print('Request failed:{0}, Reason: {1}'.format(r.status_code, r.reason))
        jsonResponse = []
        df=pd.DataFrame([])
    
    if os.path.isfile(filelocation+'fills_of_date_'+toDate+'.csv'):
        os.remove(filelocation+'fills_of_date_'+toDate+'.csv')
    df.to_csv(filelocation+'fills_of_date_'+toDate+'.csv')

def fillsInRange(startDate,endDate):
    bday_pd = pd.offsets.CustomBusinessDay( weekmask='Mon Tue Wed Thu Fri Sun')
    rangeDate=pd.date_range(start=startDate,end=endDate,freq=bday_pd).date.astype(str)
    results = []
    for date in rangeDate:
        fetchData(date)
        print('fetched for:'+date)

today=dt.datetime.today()
yesterday = today - timedelta(days = 1)
if not today.weekday()==5:
    fetchData(str('{:02d}'.format(today.year))+'-'+str('{:02d}'.format(today.month))+'-'+str('{:02d}'.format(today.day)))