import streamlit as st
import pandas as pd
import plost
from datetime import datetime
import numpy as np
from PIL import Image
#from streamlit_faker import get_streamlit_faker


this_month=str(datetime.now().year)+"/"+str(datetime.now().month)
last_month=str(datetime.now().year)+"/"+str(datetime.now().month-1)

df=pd.read_csv("c:\\Python\\TextTT_Dash\\fills_folder\\pivot.csv")
df_thisMonth=df.loc[df['year_month']==this_month]
df_lastMonth=df.loc[df['year_month']==last_month]
itm_list=df['itm'].unique()
itm_list.sort(axis=0)
product_list=df['ttProductCode'].unique()
product_list.sort(axis=0)
product_list_options=np.insert(product_list,0,"All")
itm_list_options=np.insert(itm_list,0,"All")
itm_total=len(itm_list)
algo_percent=round((df['algofill'].sum()/df['fillQty'].sum())*100,2)
algo_percent_thisMonth=round((df_thisMonth['algofill'].sum()/df_thisMonth['fillQty'].sum())*100,2)
algo_percent_lastMonth=round((df_lastMonth['algofill'].sum()/df_lastMonth['fillQty'].sum())*100,2)



st.set_page_config(layout='wide', initial_sidebar_state='expanded')
logo=Image.open("C:/Python/Git/assets/ff_logo.png")
st.sidebar.image(logo)

with open('C:/Python/Git/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Algo% Dashboard `mockup`')

st.sidebar.subheader('Select User(s)') 
itm_multiselect_choice = st.sidebar.multiselect(
    'Select User(s)',
    itm_list_options,
    "All",
    label_visibility="collapsed")

st.sidebar.subheader('Select Product(s)') 
product_multiselect_choice = st.sidebar.multiselect(
    'Select User(s)',
    product_list_options,
    "All",
    label_visibility="collapsed")

st.sidebar.markdown('''
---
Created with ❤️ by Brajesh.
''')

#Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Algo% (Annual)", algo_percent, "15%")
col2.metric("ITM", itm_total, "-2")
col3.metric("Algo% (This Month)", algo_percent_thisMonth, str(round(algo_percent_thisMonth-algo_percent_lastMonth,2))+"%")
