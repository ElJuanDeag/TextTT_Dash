import streamlit as st
import pandas as pd
import plost
from datetime import datetime
#from streamlit_faker import get_streamlit_faker

this_month=str(datetime.now().year)+"/"+str(datetime.now().month)

df=pd.read_csv("c:\\Python\\TextTT_Dash\\fills_folder\\pivot.csv")
df_thisMonth=df.loc[df['year_month']==this_month]
itm_list=df['itm'].unique()
itm_total=len(itm_list)
algo_percent=round((df['algofill'].sum()/df['fillQty'].sum())*100,2)
algo_percent_thisMonth=round((df_thisMonth['algofill'].sum()/df_thisMonth['fillQty'].sum())*100,2)



st.set_page_config(layout='wide', initial_sidebar_state='expanded')

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
st.sidebar.header('Algo% Dashboard `mockup`')

st.sidebar.subheader('Data FIlter Parameters') 
itm_choice = st.multiselect(
    'Select User(s)',
    itm_list,
    itm_list,
    label_visibility="collapsed")

st.sidebar.markdown('''
---
Created with ❤️❤️ by Brajesh.
''')

#Row A
st.markdown('### Metrics')
col1, col2, col3 = st.columns(3)
col1.metric("Algo% (Annual)", algo_percent, "5%")
col2.metric("ITM", itm_total, "-2")
col3.metric("Algo% (This Month)", algo_percent_thisMonth, "1")
