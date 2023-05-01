import os
import datetime as dt
from datetime import datetime
import requests
import json
from requests_negotiate_sspi import HttpNegotiateAuth
import pandas as pd
import numpy as np
import re
import glob
import tqdm


filelocation='C:\\Python\\TextTT_Dash\\fills_folder\\'

csv_files = glob.glob(filelocation+'fills_of_date_'+'*.csv')
df_original=pd.DataFrame()
for file in csv_files:
    df_temp = pd.read_csv(file)
    df_original= df_original.append(df_temp, ignore_index=True)

df=pd.DataFrame()
df=df_original
df.drop(['Unnamed: 0'],axis=1,inplace=True)
df['tradeDate']=pd.to_datetime(df['tradeDate'])
df['year_month']=df['tradeDate'].dt.year.astype(str)+'/'+df['tradeDate'].dt.month.astype(str)
df=df[df['securityType']=='FUTURE']
df.textTT.fillna('MANUAL',inplace=True)
df['textTT']=df['textTT'].apply(lambda x: re.search("(?<=:)[^:]*$", x).group() if ':' in x else x).str.strip()
df.to_csv(filelocation+'rawFills.csv')

def transform_row(row):
    TextTT_dict={"rangetraderprofit":"RangeTrader",
         "Rangeentry2":"RangeTrader",
          "rangetraderentry":"RangeTrader",
         "RT_ASE_Entry":"RangeTrader_Gen2",
         "RT_ASE_Exit":"RangeTrader_Gen2",
          "RRT_ASE_Entry":"RangeTrader_Gen2",
          "RRT_ASE_Exit":"RangeTrader_Gen2",
          "PRT_LimitEntry":"RangeTrader_Gen2",
          "PRT_Exit":"RangeTrader_Gen2",
          "PRT_ReEntry":"RangeTrader_Gen2",
          "PRT_FixedExit":"RangeTrader_Gen2",
          "PRT_ASE_Limit":"RangeTrader_Gen2",
          "PRT_ASE_Exit":"RangeTrader_Gen2",
         }
    if pd.isna(row['algoName']):#=='':
        if row['textTT'] in TextTT_dict:
            if row['algo']=='ASE':
                return 'ASE & '+TextTT_dict[row['textTT']]
            else:
                return TextTT_dict[row['textTT']]
        elif row['textTT'] == 'MANUAL':
            if row['algo'] == 'ASE':
                return 'ASE'
            else:
                return 'Manual'
        else:
            return 'Pvt_Algo'
    else:
        return row['algoName']

df['algoName'] = df.apply(lambda row: transform_row(row),axis=1)
df['algofill']=np.where(df['algo']=='Manual',0, df['fillQty'])
df['algofill']=np.where(df['algo']=='Manual',0, df['fillQty'])
pivot_table=df.pivot_table(index=['year_month','itm','ttProductCode', 'algo','algoName'], values=['algofill','fillQty'], aggfunc='sum').reset_index()

productdf=pd.read_csv("productClass.csv")
productClassDict=dict(zip(productdf.productCode,productdf.productClass))

batchdf=pd.read_csv("batchList.csv",names=['itm','batch'],header=None)
batchDict=dict(zip(batchdf.itm,batchdf.batch))

def get_product_class(row):
    if row['ttProductCode'] in productClassDict:
        return productClassDict[row['ttProductCode']]
    else:
        return None
    
def get_batch(row):
    if row['itm'] in batchDict:
        return batchDict[row['itm']]
    else:
        return None
    
pivot_table['productClass'] = pivot_table.apply(get_product_class, axis=1)
pivot_table['batch'] = pivot_table.apply(get_batch, axis=1)

if os.path.isfile(filelocation+'pivot.csv'):
    os.remove(filelocation+'pivot.csv')
pivot_table.to_csv(filelocation+'pivot.csv',index=False)