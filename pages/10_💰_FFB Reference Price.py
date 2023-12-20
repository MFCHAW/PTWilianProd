import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import numpy as np
from pytz import timezone
import io
import time

url = st.secrets['url_FFBRefPrice']


#################################
# Session States Initialization #
#################################
if 'ffbrefprice_Status' not in st.session_state:
    st.session_state['ffbrefprice_Status'] = ''
    
if 'ffbrefprice_Message' not in st.session_state:
    st.session_state['ffbrefprice_Message'] = ''
    
if 'ffbrefprice_OUKey' not in st.session_state:
    st.session_state['ffbrefprice_OUKey'] = -1
    
    
# New, Edit, Delete, Cancel & Submit Button Disabled Status
if 'ffbrefprice_btnNew_disabled' not in st.session_state:
    st.session_state['ffbrefprice_btnNew_disabled'] = False

if 'ffbrefprice_btnEdit_disabled' not in st.session_state: 
    st.session_state['ffbrefprice_btnEdit_disabled'] = False
    
if 'ffbrefprice_btnDelete_disabled' not in st.session_state: 
    st.session_state['ffbrefprice_btnDelete_disabled'] = False
    
if 'ffbrefprice_btnCancel_disabled' not in st.session_state: 
    st.session_state['ffbrefprice_btnCancel_disabled'] = True
    
if 'ffbrefprice_btnSubmit_disabled' not in st.session_state: 
    st.session_state['ffbrefprice_btnSubmit_disabled'] = True
    

# From Date, To Date and Grid        
today = datetime.now()
    
if 'ffbrefprice_FromDate' not in st.session_state:
    st.session_state['ffbrefprice_FromDate'] = datetime(today.year, today.month, 1)
    
if 'ffbrefprice_ToDate' not in st.session_state:
    st.session_state['ffbrefprice_ToDate'] = today

if 'ffbrefprice_RecordList' not in st.session_state:
    st.session_state['ffbrefprice_RecordList'] = []


# Mill and Date
if 'ffbrefprice_Mill' not in st.session_state:
    st.session_state['ffbrefprice_Mill'] = st.session_state['ffbrefprice_OUKey']  #'LIBO SAWIT PERKASA PALM OIL MILL'
    
if 'ffbrefprice_Date' not in st.session_state:
    st.session_state['ffbrefprice_Date'] = datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S")

if 'ffbrefprice_Date_disabled' not in st.session_state:
    st.session_state['ffbrefprice_Date_disabled'] = True
    
    
# CPO Price    
if 'ffbrefprice_CPOTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_CPOTdPrice'] = 0.00
    
if 'ffbrefprice_CPOTdPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_CPOTdPrice_disabled'] = True

if 'ffbrefprice_CPOSellPrice' not in st.session_state:
    st.session_state['ffbrefprice_CPOSellPrice'] = 0.00
    
if 'ffbrefprice_CPOSellPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_CPOSellPrice_disabled'] = True
    
if 'ffbrefprice_CPOProCharges' not in st.session_state:
    st.session_state['ffbrefprice_CPOProCharges'] = 0.00
    
if 'ffbrefprice_CPOProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_CPOProCharges_disabled'] = True
    
if 'ffbrefprice_CPORealProCharges' not in st.session_state:
    st.session_state['ffbrefprice_CPORealProCharges'] = 0.00
    
if 'ffbrefprice_CPORealProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_CPORealProCharges_disabled'] = True   
    
if 'ffbrefprice_CPOTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_CPOTransCharges'] = 0.00

if 'ffbrefprice_CPOTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_CPOTransCharges_disabled'] = True
    
if 'ffbrefprice_RendCPO' not in st.session_state:
    st.session_state['ffbrefprice_RendCPO'] = 0.00

if 'ffbrefprice_RendCPO_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RendCPO_disabled'] = True   
    

# PK Price
if 'ffbrefprice_PKTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_PKTdPrice'] = 0.00
    
if 'ffbrefprice_PKTdPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_PKTdPrice_disabled'] = True
    
if 'ffbrefprice_PKSellPrice' not in st.session_state:
    st.session_state['ffbrefprice_PKSellPrice'] = 0.00
    
if 'ffbrefprice_PKSellPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_PKSellPrice_disabled'] = True 

if 'ffbrefprice_PKProCharges' not in st.session_state:
    st.session_state['ffbrefprice_PKProCharges'] = 0.00

if 'ffbrefprice_PKProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_PKProCharges_disabled'] = True
    
if 'ffbrefprice_PKRealProCharges' not in st.session_state:
    st.session_state['ffbrefprice_PKRealProCharges'] = 0.00

if 'ffbrefprice_PKRealProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_PKRealProCharges_disabled'] = True
    
if 'ffbrefprice_PKTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_PKTransCharges'] = 0.00

if 'ffbrefprice_PKTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_PKTransCharges_disabled'] = True

if 'ffbrefprice_RendPK' not in st.session_state:
    st.session_state['ffbrefprice_RendPK'] = 0.00

if 'ffbrefprice_RendPK_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RendPK_disabled'] = True


# Shell Price  
if 'ffbrefprice_ShellTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ShellTdPrice'] = 0.00

if 'ffbrefprice_ShellTdPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ShellTdPrice_disabled'] = True

if 'ffbrefprice_ShellSellPrice' not in st.session_state:
    st.session_state['ffbrefprice_ShellSellPrice'] = 0.00

if 'ffbrefprice_ShellSellPrice_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ShellSellPrice_disabled'] = True  

if 'ffbrefprice_ShellProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ShellProCharges'] = 0.00

if 'ffbrefprice_ShellProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ShellProCharges_disabled'] = True
    
if 'ffbrefprice_ShellRealProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ShellRealProCharges'] = 0.00

if 'ffbrefprice_ShellRealProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ShellRealProCharges_disabled'] = True  
    
if 'ffbrefprice_ShellTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ShellTransCharges'] = 0.00

if 'ffbrefprice_ShellTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ShellTransCharges_disabled'] = True

if 'ffbrefprice_RendShell' not in st.session_state:
    st.session_state['ffbrefprice_RendShell'] = 0.00

if 'ffbrefprice_RendShell_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RendShell_disabled'] = True
    

# CPO Price (Excl. PPN)
if 'ffbrefprice_ETaxCPOTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOTdPrice'] = 0.00

if 'ffbrefprice_ETaxCPO' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPO'] = 0.00
    
if 'ffbrefprice_ETaxCPO_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPO_disabled'] = True

if 'ffbrefprice_ETaxCPOProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOProCharges'] = 0.00
    
if 'ffbrefprice_ETaxCPOProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOProCharges_disabled'] = True   

if 'ffbrefprice_ETaxCPOTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOTransCharges'] = 0.00
    
if 'ffbrefprice_ETaxCPOTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOTransCharges_disabled'] = True 

if 'ffbrefprice_ETaxRendCPO' not in st.session_state:
    st.session_state['ffbrefprice_ETaxRendCPO'] = 0.00 
    
if 'ffbrefprice_ETaxCPOPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxCPOPrice'] = 0.00   


# PK Price (Excl. PPN)
if 'ffbrefprice_ETaxPKTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKTdPrice'] = 0.00

if 'ffbrefprice_ETaxPK' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPK'] = 0.00
    
if 'ffbrefprice_ETaxPK_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPK_disabled'] = True

if 'ffbrefprice_ETaxPKProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKProCharges'] = 0.00
    
if 'ffbrefprice_ETaxPKProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKProCharges_disabled'] = True   

if 'ffbrefprice_ETaxPKTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKTransCharges'] = 0.00
    
if 'ffbrefprice_ETaxPKTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKTransCharges_disabled'] = True 
    
if 'ffbrefprice_ETaxRendPK' not in st.session_state:
    st.session_state['ffbrefprice_ETaxRendPK'] = 0.00 
    
if 'ffbrefprice_ETaxPKPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxPKPrice'] = 0.00 


# Shell Price (Excl. PPN)
if 'ffbrefprice_ETaxShellTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellTdPrice'] = 0.00

if 'ffbrefprice_ETaxShell' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShell'] = 0.00
    
if 'ffbrefprice_ETaxShell_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShell_disabled'] = True

if 'ffbrefprice_ETaxShellProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellProCharges'] = 0.00
    
if 'ffbrefprice_ETaxShellProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellProCharges_disabled'] = True   

if 'ffbrefprice_ETaxShellTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellTransCharges'] = 0.00
    
if 'ffbrefprice_ETaxShellTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellTransCharges_disabled'] = True 

if 'ffbrefprice_ETaxRendShell' not in st.session_state:
    st.session_state['ffbrefprice_ETaxRendShell'] = 0.00 
    
if 'ffbrefprice_ETaxShellPrice' not in st.session_state:
    st.session_state['ffbrefprice_ETaxShellPrice'] = 0.00


# CPO Price (Incl. PPN)
if 'ffbrefprice_ITaxCPOTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOTdPrice'] = 0.00

if 'ffbrefprice_ITaxCPO' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPO'] = 0.00
    
if 'ffbrefprice_ITaxCPO_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPO_disabled'] = True

if 'ffbrefprice_ITaxCPOProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOProCharges'] = 0.00
    
if 'ffbrefprice_ITaxCPOProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOProCharges_disabled'] = True   

if 'ffbrefprice_ITaxCPOTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOTransCharges'] = 0.00
    
if 'ffbrefprice_ITaxCPOTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOTransCharges_disabled'] = True 

if 'ffbrefprice_ITaxRendCPO' not in st.session_state:
    st.session_state['ffbrefprice_ITaxRendCPO'] = 0.00 
    
if 'ffbrefprice_ITaxCPOPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxCPOPrice'] = 0.00  


# PK Price (Incl. PPN)
if 'ffbrefprice_ITaxPKTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKTdPrice'] = 0.00

if 'ffbrefprice_ITaxPK' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPK'] = 0.00
    
if 'ffbrefprice_ITaxPK_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPK_disabled'] = True

if 'ffbrefprice_ITaxPKProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKProCharges'] = 0.00
    
if 'ffbrefprice_ITaxPKProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKProCharges_disabled'] = True   

if 'ffbrefprice_ITaxPKTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKTransCharges'] = 0.00
    
if 'ffbrefprice_ITaxPKTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKTransCharges_disabled'] = True 
    
if 'ffbrefprice_ITaxRendPK' not in st.session_state:
    st.session_state['ffbrefprice_ITaxRendPK'] = 0.00 
    
if 'ffbrefprice_ITaxPKPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxPKPrice'] = 0.00 


# Shell Price (Incl. PPN)
if 'ffbrefprice_ITaxShellTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellTdPrice'] = 0.00

if 'ffbrefprice_ITaxShell' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShell'] = 0.00
    
if 'ffbrefprice_ITaxShell_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShell_disabled'] = True

if 'ffbrefprice_ITaxShellProCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellProCharges'] = 0.00
    
if 'ffbrefprice_ITaxShellProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellProCharges_disabled'] = True   

if 'ffbrefprice_ITaxShellTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellTransCharges'] = 0.00
    
if 'ffbrefprice_ITaxShellTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellTransCharges_disabled'] = True 

if 'ffbrefprice_ITaxRendShell' not in st.session_state:
    st.session_state['ffbrefprice_ITaxRendShell'] = 0.00 
    
if 'ffbrefprice_ITaxShellPrice' not in st.session_state:
    st.session_state['ffbrefprice_ITaxShellPrice'] = 0.00


# CPO Price (FFB Price Per Kg (Actual Production))
if 'ffbrefprice_RCPOTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_RCPOTdPrice'] = 0.00

if 'ffbrefprice_RTaxCPO' not in st.session_state:
    st.session_state['ffbrefprice_RTaxCPO'] = 0.00
    
if 'ffbrefprice_RTaxCPO_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RTaxCPO_disabled'] = True

if 'ffbrefprice_RCPOProCharges' not in st.session_state:
    st.session_state['ffbrefprice_RCPOProCharges'] = 0.00
    
if 'ffbrefprice_RCPOProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RCPOProCharges_disabled'] = True   

if 'ffbrefprice_RCPOTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_RCPOTransCharges'] = 0.00
    
if 'ffbrefprice_RCPOTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RCPOTransCharges_disabled'] = True 

if 'ffbrefprice_RRendCPO' not in st.session_state:
    st.session_state['ffbrefprice_RRendCPO'] = 0.00 
    
if 'ffbrefprice_RCPOPrice' not in st.session_state:
    st.session_state['ffbrefprice_RCPOPrice'] = 0.00  


# PK Price (FFB Price Per Kg (Actual Production))
if 'ffbrefprice_RPKTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_RPKTdPrice'] = 0.00

if 'ffbrefprice_RTaxPK' not in st.session_state:
    st.session_state['ffbrefprice_RTaxPK'] = 0.00
    
if 'ffbrefprice_RTaxPK_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RTaxPK_disabled'] = True

if 'ffbrefprice_RPKProCharges' not in st.session_state:
    st.session_state['ffbrefprice_RPKProCharges'] = 0.00
    
if 'ffbrefprice_RPKProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RPKProCharges_disabled'] = True   

if 'ffbrefprice_RPKTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_RPKTransCharges'] = 0.00
    
if 'ffbrefprice_RPKTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RPKTransCharges_disabled'] = True 

if 'ffbrefprice_RRendPK' not in st.session_state:
    st.session_state['ffbrefprice_RRendPK'] = 0.00 
    
if 'ffbrefprice_RPKPrice' not in st.session_state:
    st.session_state['ffbrefprice_RPKPrice'] = 0.00
    

# Shell Price (FFB Price Per Kg (Actual Production))
if 'ffbrefprice_RShellTdPrice' not in st.session_state:
    st.session_state['ffbrefprice_RShellTdPrice'] = 0.00

if 'ffbrefprice_RTaxShell' not in st.session_state:
    st.session_state['ffbrefprice_RTaxShell'] = 0.00
    
if 'ffbrefprice_RTaxShell_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RTaxShell_disabled'] = True

if 'ffbrefprice_RShellProCharges' not in st.session_state:
    st.session_state['ffbrefprice_RShellProCharges'] = 0.00
    
if 'ffbrefprice_RShellProCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RShellProCharges_disabled'] = True   

if 'ffbrefprice_RShellTransCharges' not in st.session_state:
    st.session_state['ffbrefprice_RShellTransCharges'] = 0.00
    
if 'ffbrefprice_RShellTransCharges_disabled' not in st.session_state:
    st.session_state['ffbrefprice_RShellTransCharges_disabled'] = True 

if 'ffbrefprice_RRendShell' not in st.session_state:
    st.session_state['ffbrefprice_RRendShell'] = 0.00 
    
if 'ffbrefprice_RShellPrice' not in st.session_state:
    st.session_state['ffbrefprice_RShellPrice'] = 0.00
    

# FFB Price List
if 'ffbrefprice_FFBPriceList' not in st.session_state:
    st.session_state['ffbrefprice_FFBPriceList'] = []


    
    
# --- Auto Navigate to Login form if haven't login yet --
if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()
    
# -- Remove the 'Streamlit' label at Page title --  
def set_page_title(title):
    st.sidebar.markdown(unsafe_allow_html=True, body=f"""
        <iframe height=0 srcdoc="<script>
            const title = window.parent.document.querySelector('title') \
                
            const oldObserver = window.parent.titleObserver
            if (oldObserver) {{
                oldObserver.disconnect()
            }} \

            const newObserver = new MutationObserver(function(mutations) {{
                const target = mutations[0].target
                if (target.text !== '{title}') {{
                    target.text = '{title}'
                }}
            }}) \

            newObserver.observe(title, {{ childList: true }})
            window.parent.titleObserver = newObserver \

            title.text = '{title}'
        </script>" />
    """)


set_page_title("PT Wilian - FFB Procurement")


# --- Display Client Logo ---
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://lmquartobistorage.blob.core.windows.net/pt-wilian-perkasa/PTWP_Logo.png');
                background-repeat: no-repeat;
                padding-top: 10px;
                background-position: 20px 25px;
            }
            # [data-testid="stSidebarNav"]::before {
            #     content: "FFB Procurement Application";
            #     margin-left: 10px;
            #     margin-top: 20px;
            #     font-size: 19px;
            #     position: relative;
            #     top: 100px;
            # }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_logo()


# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


# -- Declare containers --
pageSection = st.container()
placeholder = st.empty()
statusMsgSection = st.container()
retrySection = st.container()





# -- Get Operating Unit Key --
def get_OUKey(ou):
    if ou == 'LIBO SAWIT PERKASA PALM OIL MILL':
        st.session_state['ffbrefprice_OUKey'] = 6
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 1':
        st.session_state['ffbrefprice_OUKey'] = 8
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 2':
        st.session_state['ffbrefprice_OUKey'] = 9


# -- Trigger Azure Logic App to submit FFB Reference Price --
async def SubmitRefPrice(Date, OUKey, 
                        CPOTdPrice, CPOSellPrice, CPOProCharges, CPORealProCharges, CPOTransCharges, RendCPO, 
                        PKTdPrice, PKSellPrice, PKProCharges, PKRealProCharges, PKTransCharges, RendPK,
                        ShellTdPrice, ShellSellPrice, ShellProCharges, ShellRealProCharges, ShellTransCharges, RendShell,
                        ETaxCPO, ETaxCPOProCharges, ETaxCPOTransCharges, ETaxCPOPrice,
                        ETaxPK, ETaxPKProCharges, ETaxPKTransCharges, ETaxPKPrice,
                        ETaxShell, ETaxShellProCharges, ETaxShellTransCharges, ETaxShellPrice,
                        ITaxCPO, ITaxCPOProCharges, ITaxCPOTransCharges, ITaxCPOPrice,
                        ITaxPK, ITaxPKProCharges, ITaxPKTransCharges, ITaxPKPrice,
                        ITaxShell, ITaxShellProCharges, ITaxShellTransCharges, ITaxShellPrice,
                        RTaxCPO, RCPOProCharges, RCPOTransCharges, RCPOPrice,
                        RTaxPK, RPKProCharges, RPKTransCharges, RPKPrice,
                        RTaxShell, RShellProCharges, RShellTransCharges, RShellPrice
                        ):

    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Submit FFB Reference Price',
            "Date": str(Date),
            "OUKey": OUKey,
            "CPOTdPrice": CPOTdPrice,
            "CPOSellPrice": CPOSellPrice,
            "CPOProCharges":CPOProCharges,
            "CPORealProCharges":CPORealProCharges,
            "CPOTransCharges": CPOTransCharges,
            "RendCPO": RendCPO,
            "PKTdPrice": PKTdPrice,
            "PKSellPrice": PKSellPrice,
            "PKProCharges": PKProCharges,
            "PKRealProCharges": PKRealProCharges,
            "PKTransCharges": PKTransCharges,
            "RendPK": RendPK,
            "ShellTdPrice": ShellTdPrice,
            "ShellSellPrice": ShellSellPrice,
            "ShellProCharges": ShellProCharges,
            "ShellRealProCharges": ShellRealProCharges,
            "ShellTransCharges": ShellTransCharges,
            "RendShell": RendShell,
            "ETaxCPO": ETaxCPO,
            "ETaxCPOProCharges": ETaxCPOProCharges,
            "ETaxCPOTransCharges": ETaxCPOTransCharges,
            "ETaxCPOPrice": float(st.session_state['ffbrefprice_ETaxCPOPrice']), # float(ETaxCPOPrice),
            "ETaxPK": ETaxPK,
            "ETaxPKProCharges": ETaxPKProCharges,
            "ETaxPKTransCharges": ETaxPKTransCharges,
            "ETaxPKPrice": float(st.session_state['ffbrefprice_ETaxPKPrice']),  # float(ETaxPKPrice),
            "ETaxShell": ETaxShell,
            "ETaxShellProCharges": ETaxShellProCharges,
            "ETaxShellTransCharges": ETaxShellTransCharges,
            "ETaxShellPrice": float(st.session_state['ffbrefprice_ETaxShellPrice']),   # float(ETaxShellPrice),
            "ITaxCPO": ITaxCPO,
            "ITaxCPOProCharges": ITaxCPOProCharges,
            "ITaxCPOTransCharges": ITaxCPOTransCharges,
            "ITaxCPOPrice": float(st.session_state['ffbrefprice_ITaxCPOPrice']), # float(ITaxCPOPrice),
            "ITaxPK": ITaxPK,
            "ITaxPKProCharges": ITaxPKProCharges,
            "ITaxPKTransCharges": ITaxPKTransCharges,
            "ITaxPKPrice": float(st.session_state['ffbrefprice_ITaxPKPrice']), # float(ITaxPKPrice),
            "ITaxShell": ITaxShell,
            "ITaxShellProCharges": ITaxShellProCharges,
            "ITaxShellTransCharges": ITaxShellTransCharges,
            "ITaxShellPrice": float(st.session_state['ffbrefprice_ITaxShellPrice']),   # float(ITaxShellPrice),
            "RTaxCPO": RTaxCPO,
            "RCPOProCharges": RCPOProCharges,
            "RCPOTransCharges": RCPOTransCharges,
            "RCPOPrice": float(st.session_state['ffbrefprice_RCPOPrice']),    # float(RCPOPrice),
            "RTaxPK": RTaxPK,
            "RPKProCharges": RPKProCharges,
            "RPKTransCharges": RPKTransCharges,
            "RPKPrice": float(st.session_state['ffbrefprice_RPKPrice']),   # float(RPKPrice),
            "RTaxShell": RTaxShell,
            "RShellProCharges": RShellProCharges,
            "RShellTransCharges": RShellTransCharges,
            "RShellPrice": float(st.session_state['ffbrefprice_RShellPrice']), # float(RShellPrice),
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            st.session_state['ffbrefprice_Status'] = ''
            Cancel()
            
            st.session_state['ffbrefprice_btnNew_disabled'] = False
            st.session_state['ffbrefprice_btnEdit_disabled'] = False
            st.session_state['ffbrefprice_btnDelete_disabled'] = False
            st.session_state['ffbrefprice_btnCancel_disabled'] = True
            st.session_state['ffbrefprice_btnSubmit_disabled'] = True
            

def Submit(Date, OUKey, 
            CPOTdPrice, CPOSellPrice, CPOProCharges, CPORealProCharges, CPOTransCharges, RendCPO, 
            PKTdPrice, PKSellPrice, PKProCharges, PKRealProCharges, PKTransCharges, RendPK,
            ShellTdPrice, ShellSellPrice, ShellProCharges, ShellRealProCharges, ShellTransCharges, RendShell,
            ETaxCPO, ETaxCPOProCharges, ETaxCPOTransCharges, ETaxCPOPrice,
            ETaxPK, ETaxPKProCharges, ETaxPKTransCharges, ETaxPKPrice,
            ETaxShell, ETaxShellProCharges, ETaxShellTransCharges, ETaxShellPrice,
            ITaxCPO, ITaxCPOProCharges, ITaxCPOTransCharges, ITaxCPOPrice,
            ITaxPK, ITaxPKProCharges, ITaxPKTransCharges, ITaxPKPrice,
            ITaxShell, ITaxShellProCharges, ITaxShellTransCharges, ITaxShellPrice,
            RTaxCPO, RCPOProCharges, RCPOTransCharges, RCPOPrice,
            RTaxPK, RPKProCharges, RPKTransCharges, RPKPrice,
            RTaxShell, RShellProCharges, RShellTransCharges, RShellPrice
            ):
    
    st.session_state['ffbrefprice_Status'] = 'Submit'
    st.session_state['ffbrefprice_Message'] = 'Submitting...'
    
    st.session_state['ffbrefprice_btnNew_disabled'] = True
    st.session_state['ffbrefprice_btnEdit_disabled'] = True
    st.session_state['ffbrefprice_btnDelete_disabled'] = True
    st.session_state['ffbrefprice_btnCancel_disabled'] = True
    st.session_state['ffbrefprice_btnSubmit_disabled'] = True
    
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(SubmitRefPrice(Date, OUKey, 
                                            CPOTdPrice, CPOSellPrice, CPOProCharges, CPORealProCharges, CPOTransCharges, RendCPO, 
                                            PKTdPrice, PKSellPrice, PKProCharges, PKRealProCharges, PKTransCharges, RendPK,
                                            ShellTdPrice, ShellSellPrice, ShellProCharges, ShellRealProCharges, ShellTransCharges, RendShell,
                                            ETaxCPO, ETaxCPOProCharges, ETaxCPOTransCharges, ETaxCPOPrice,
                                            ETaxPK, ETaxPKProCharges, ETaxPKTransCharges, ETaxPKPrice,
                                            ETaxShell, ETaxShellProCharges, ETaxShellTransCharges, ETaxShellPrice,
                                            ITaxCPO, ITaxCPOProCharges, ITaxCPOTransCharges, ITaxCPOPrice,
                                            ITaxPK, ITaxPKProCharges, ITaxPKTransCharges, ITaxPKPrice,
                                            ITaxShell, ITaxShellProCharges, ITaxShellTransCharges, ITaxShellPrice,
                                            RTaxCPO, RCPOProCharges, RCPOTransCharges, RCPOPrice,
                                            RTaxPK, RPKProCharges, RPKTransCharges, RPKPrice,
                                            RTaxShell, RShellProCharges, RShellTransCharges, RShellPrice)) 
    
    Call_DisplayGridRecords(st.session_state['ffbrefprice_OUKey'], st.session_state['ffbrefprice_FromDate'], st.session_state['ffbrefprice_ToDate'])   
    
    st.markdown('#')
    
async def DisplayGridRecords(OUKey, FromDate, ToDate):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Load Record List',
            "OUKey": OUKey,
            "FromDate": str(FromDate),
            "ToDate": str(ToDate)
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            if len(data['ResultSets']) != 0:
                df = pd.DataFrame(data['ResultSets']['Table1'])
                st.session_state['ffbrefprice_RecordList'] = df
            else:
                st.session_state['ffbrefprice_RecordList'] = []

async def DisplayFFBPriceRecords(OUKey, Date):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Load FFB Price List',
            "OUKey": OUKey,
            "Date": str(Date)
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            if len(data['ResultSets']) != 0:
                df = pd.DataFrame(data['ResultSets']['Table1'])
                st.session_state['ffbrefprice_FFBPriceList'] = df
            else:
                st.session_state['ffbrefprice_FFBPriceList'] = []


def Call_DisplayGridRecords(OUKey, fromDate, toDate):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DisplayGridRecords(OUKey, fromDate, toDate)) 

   
def Call_DisplayFFBPriceRecords(ouKey, Date):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DisplayFFBPriceRecords(ouKey, Date)) 
    

def New():
    st.session_state['ffbrefprice_btnNew_disabled'] = True
    st.session_state['ffbrefprice_btnEdit_disabled'] = True
    st.session_state['ffbrefprice_btnDelete_disabled'] = True
    st.session_state['ffbrefprice_btnCancel_disabled'] = False
    st.session_state['ffbrefprice_btnSubmit_disabled'] = False
    
    st.session_state['ffbrefprice_Status'] = 'New'
    st.session_state['ffbrefprice_Message'] = 'Adding New Record'
    
    st.session_state['ffbrefprice_Date_disabled'] = False
    
    EmptyRecords()
    ControlAllowEdit()

    
def ControlAllowEdit():
    st.session_state['ffbrefprice_CPOTdPrice_disabled'] = False
    st.session_state['ffbrefprice_CPOSellPrice_disabled'] = False
    st.session_state['ffbrefprice_CPOProCharges_disabled'] = False
    st.session_state['ffbrefprice_CPORealProCharges_disabled'] = False
    st.session_state['ffbrefprice_CPOTransCharges_disabled'] = False
    st.session_state['ffbrefprice_RendCPO_disabled'] = False
    
    st.session_state['ffbrefprice_PKTdPrice_disabled'] = False
    st.session_state['ffbrefprice_PKSellPrice_disabled'] = False
    st.session_state['ffbrefprice_PKProCharges_disabled'] = False
    st.session_state['ffbrefprice_PKRealProCharges_disabled'] = False
    st.session_state['ffbrefprice_PKTransCharges_disabled'] = False
    st.session_state['ffbrefprice_RendPK_disabled'] = False
    
    st.session_state['ffbrefprice_ShellTdPrice_disabled'] = False
    st.session_state['ffbrefprice_ShellSellPrice_disabled'] = False
    st.session_state['ffbrefprice_ShellProCharges_disabled'] = False
    st.session_state['ffbrefprice_ShellRealProCharges_disabled'] = False
    st.session_state['ffbrefprice_ShellTransCharges_disabled'] = False
    st.session_state['ffbrefprice_RendShell_disabled'] = False
    
    st.session_state['ffbrefprice_ETaxCPO_disabled'] = False
    st.session_state['ffbrefprice_ETaxCPOProCharges_disabled'] = False
    st.session_state['ffbrefprice_ETaxCPOTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_ETaxPK_disabled'] = False
    st.session_state['ffbrefprice_ETaxPKProCharges_disabled'] = False
    st.session_state['ffbrefprice_ETaxPKTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_ETaxShell_disabled'] = False
    st.session_state['ffbrefprice_ETaxShellProCharges_disabled'] = False
    st.session_state['ffbrefprice_ETaxShellTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_ITaxCPO_disabled'] = False
    st.session_state['ffbrefprice_ITaxCPOProCharges_disabled'] = False
    st.session_state['ffbrefprice_ITaxCPOTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_ITaxPK_disabled'] = False
    st.session_state['ffbrefprice_ITaxPKProCharges_disabled'] = False
    st.session_state['ffbrefprice_ITaxPKTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_ITaxShell_disabled'] = False
    st.session_state['ffbrefprice_ITaxShellProCharges_disabled'] = False
    st.session_state['ffbrefprice_ITaxShellTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_RTaxCPO_disabled'] = False
    st.session_state['ffbrefprice_RCPOProCharges_disabled'] = False
    st.session_state['ffbrefprice_RCPOTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_RTaxPK_disabled'] = False
    st.session_state['ffbrefprice_RPKProCharges_disabled'] = False
    st.session_state['ffbrefprice_RPKTransCharges_disabled'] = False
    
    st.session_state['ffbrefprice_RTaxShell_disabled'] = False
    st.session_state['ffbrefprice_RShellProCharges_disabled'] = False
    st.session_state['ffbrefprice_RShellTransCharges_disabled'] = False
    
    
def ControlNotAllowEdit():
    st.session_state['ffbrefprice_CPOTdPrice_disabled'] = True
    st.session_state['ffbrefprice_CPOSellPrice_disabled'] = True
    st.session_state['ffbrefprice_CPOProCharges_disabled'] = True
    st.session_state['ffbrefprice_CPORealProCharges_disabled'] = True
    st.session_state['ffbrefprice_CPOTransCharges_disabled'] = True
    st.session_state['ffbrefprice_RendCPO_disabled'] = True
    
    st.session_state['ffbrefprice_PKTdPrice_disabled'] = True
    st.session_state['ffbrefprice_PKSellPrice_disabled'] = True
    st.session_state['ffbrefprice_PKProCharges_disabled'] = True
    st.session_state['ffbrefprice_PKRealProCharges_disabled'] = True
    st.session_state['ffbrefprice_PKTransCharges_disabled'] = True
    st.session_state['ffbrefprice_RendPK_disabled'] = True
    
    st.session_state['ffbrefprice_ShellTdPrice_disabled'] = True
    st.session_state['ffbrefprice_ShellSellPrice_disabled'] = True
    st.session_state['ffbrefprice_ShellProCharges_disabled'] = True
    st.session_state['ffbrefprice_ShellRealProCharges_disabled'] = True
    st.session_state['ffbrefprice_ShellTransCharges_disabled'] = True
    st.session_state['ffbrefprice_RendShell_disabled'] = True
    
    st.session_state['ffbrefprice_ETaxCPO_disabled'] = True
    st.session_state['ffbrefprice_ETaxCPOProCharges_disabled'] = True
    st.session_state['ffbrefprice_ETaxCPOTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_ETaxPK_disabled'] = True
    st.session_state['ffbrefprice_ETaxPKProCharges_disabled'] = True
    st.session_state['ffbrefprice_ETaxPKTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_ETaxShell_disabled'] = True
    st.session_state['ffbrefprice_ETaxShellProCharges_disabled'] = True
    st.session_state['ffbrefprice_ETaxShellTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_ITaxCPO_disabled'] = True
    st.session_state['ffbrefprice_ITaxCPOProCharges_disabled'] = True
    st.session_state['ffbrefprice_ITaxCPOTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_ITaxPK_disabled'] = True
    st.session_state['ffbrefprice_ITaxPKProCharges_disabled'] = True
    st.session_state['ffbrefprice_ITaxPKTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_ITaxShell_disabled'] = True
    st.session_state['ffbrefprice_ITaxShellProCharges_disabled'] = True
    st.session_state['ffbrefprice_ITaxShellTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_RTaxCPO_disabled'] = True
    st.session_state['ffbrefprice_RCPOProCharges_disabled'] = True
    st.session_state['ffbrefprice_RCPOTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_RTaxPK_disabled'] = True
    st.session_state['ffbrefprice_RPKProCharges_disabled'] = True
    st.session_state['ffbrefprice_RPKTransCharges_disabled'] = True
    
    st.session_state['ffbrefprice_RTaxShell_disabled'] = True
    st.session_state['ffbrefprice_RShellProCharges_disabled'] = True
    st.session_state['ffbrefprice_RShellTransCharges_disabled'] = True


def EmptyRecords():
    
    st.session_state['ffbrefprice_Date'] = datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S")
    
    # CPO Price
    st.session_state['ffbrefprice_CPOTdPrice'] = 0.00
    st.session_state['ffbrefprice_CPOSellPrice'] = 0.00
    st.session_state['ffbrefprice_CPOProCharges'] = 0.00
    st.session_state['ffbrefprice_CPORealProCharges'] = 0.00
    st.session_state['ffbrefprice_CPOTransCharges'] = 0.00
    st.session_state['ffbrefprice_RendCPO'] = 0.00
    
    # PK Price
    st.session_state['ffbrefprice_PKTdPrice'] = 0.00
    st.session_state['ffbrefprice_PKSellPrice'] = 0.00
    st.session_state['ffbrefprice_PKProCharges'] = 0.00
    st.session_state['ffbrefprice_PKRealProCharges'] = 0.00
    st.session_state['ffbrefprice_PKTransCharges'] = 0.00
    st.session_state['ffbrefprice_RendPK'] = 0.00
    
    # Shell Price
    st.session_state['ffbrefprice_ShellTdPrice'] = 0.00
    st.session_state['ffbrefprice_ShellSellPrice'] = 0.00
    st.session_state['ffbrefprice_ShellProCharges'] = 0.00
    st.session_state['ffbrefprice_ShellRealProCharges'] = 0.00
    st.session_state['ffbrefprice_ShellTransCharges'] = 0.00
    st.session_state['ffbrefprice_RendShell'] = 0.00
    
    # CPO (Excl. PPN)
    st.session_state['ffbrefprice_ETaxCPOTdPrice'] = 0.00
    st.session_state['ffbrefprice_ETaxCPO'] = 0.00
    st.session_state['ffbrefprice_ETaxCPOProCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxCPOTransCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxRendCPO'] = 0.00
    st.session_state['ffbrefprice_ETaxCPOPrice'] = 0.00
    
    # PK (Excl. PPN)
    st.session_state['ffbrefprice_ETaxPKTdPrice'] = 0.00
    st.session_state['ffbrefprice_ETaxPK'] = 0.00
    st.session_state['ffbrefprice_ETaxPKProCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxPKTransCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxRendPK'] = 0.00
    st.session_state['ffbrefprice_ETaxPKPrice'] = 0.00
    
    # Shell (Excl. PPN)
    st.session_state['ffbrefprice_ETaxShellTdPrice'] = 0.00
    st.session_state['ffbrefprice_ETaxShell'] = 0.00
    st.session_state['ffbrefprice_ETaxShellProCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxShellTransCharges'] = 0.00
    st.session_state['ffbrefprice_ETaxRendShell'] = 0.00
    st.session_state['ffbrefprice_ETaxShellPrice'] = 0.00
    
    # CPO (Incl. PPN)
    st.session_state['ffbrefprice_ITaxCPOTdPrice'] = 0.00
    st.session_state['ffbrefprice_ITaxCPO'] = 0.00
    st.session_state['ffbrefprice_ITaxCPOProCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxCPOTransCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxRendCPO'] = 0.00
    st.session_state['ffbrefprice_ITaxCPOPrice'] = 0.00
    
     # PK (Incl. PPN)
    st.session_state['ffbrefprice_ITaxPKTdPrice'] = 0.00
    st.session_state['ffbrefprice_ITaxPK'] = 0.00
    st.session_state['ffbrefprice_ITaxPKProCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxPKTransCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxRendPK'] = 0.00
    st.session_state['ffbrefprice_ITaxPKPrice'] = 0.00
    
    # Shell (Incl. PPN)
    st.session_state['ffbrefprice_ITaxShellTdPrice'] = 0.00
    st.session_state['ffbrefprice_ITaxShell'] = 0.00
    st.session_state['ffbrefprice_ITaxShellProCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxShellTransCharges'] = 0.00
    st.session_state['ffbrefprice_ITaxRendShell'] = 0.00
    st.session_state['ffbrefprice_ITaxShellPrice'] = 0.00
    
    # CPO (FFB Price Per Kg (Actual Production))
    st.session_state['ffbrefprice_RCPOTdPrice'] = 0.00
    st.session_state['ffbrefprice_RTaxCPO'] = 0.00
    st.session_state['ffbrefprice_RCPOProCharges'] = 0.00
    st.session_state['ffbrefprice_RCPOTransCharges'] = 0.00
    st.session_state['ffbrefprice_RRendCPO'] = 0.00
    st.session_state['ffbrefprice_RCPOPrice'] = 0.00
    
    # PK (FFB Price Per Kg (Actual Production))
    st.session_state['ffbrefprice_RPKTdPrice'] = 0.00
    st.session_state['ffbrefprice_RTaxPK'] = 0.00
    st.session_state['ffbrefprice_RPKProCharges'] = 0.00
    st.session_state['ffbrefprice_RPKTransCharges'] = 0.00
    st.session_state['ffbrefprice_RRendPK'] = 0.00
    st.session_state['ffbrefprice_RPKPrice'] = 0.00
    
    # Shell (FFB Price Per Kg (Actual Production))
    st.session_state['ffbrefprice_RShellTdPrice'] = 0.00
    st.session_state['ffbrefprice_RTaxShell'] = 0.00
    st.session_state['ffbrefprice_RShellProCharges'] = 0.00
    st.session_state['ffbrefprice_RShellTransCharges'] = 0.00
    st.session_state['ffbrefprice_RRendShell'] = 0.00
    st.session_state['ffbrefprice_RShellPrice'] = 0.00
    
 
def Edit():
    st.session_state['ffbrefprice_Status'] = 'Edit'
    st.session_state['ffbrefprice_btnNew_disabled'] = True
    st.session_state['ffbrefprice_btnEdit_disabled'] = True
    st.session_state['ffbrefprice_btnDelete_disabled'] = True
    st.session_state['ffbrefprice_btnCancel_disabled'] = False
    st.session_state['ffbrefprice_btnSubmit_disabled'] = False
    
    st.session_state['ffbrefprice_Date_disabled'] = False
    
    ControlAllowEdit()
    
    
# -- Trigger Azure Logic App to delete FFB Reference Price --
async def DeleteFFBRefPrice(Date, OUKey):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Delete FFB Reference Price',
            "Date": str(Date),
            "OUKey": OUKey,
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
             
            

def Delete(Date, OUKey):
    st.session_state['ffbrefprice_Status'] = 'Delete Record'
    st.session_state['ffbrefprice_Message'] = 'Deleting Record...'
    
    st.session_state['ffbrefprice_btnNew_disabled'] = True
    st.session_state['ffbrefprice_btnEdit_disabled'] = True
    st.session_state['ffbrefprice_btnDelete_disabled'] = True
    st.session_state['ffbrefprice_btnCancel_disabled'] = True
    st.session_state['ffbrefprice_btnSubmit_disabled'] = True
    
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DeleteFFBRefPrice(Date, OUKey)) 
    
    Call_DisplayGridRecords(st.session_state['ffbrefprice_OUKey'], st.session_state['ffbrefprice_FromDate'], st.session_state['ffbrefprice_ToDate'])   
    EmptyRecords()
    Cancel()
            
    st.session_state['ffbrefprice_btnNew_disabled'] = False
    st.session_state['ffbrefprice_btnEdit_disabled'] = False
    st.session_state['ffbrefprice_btnDelete_disabled'] = False
    st.session_state['ffbrefprice_btnCancel_disabled'] = True
    st.session_state['ffbrefprice_btnSubmit_disabled'] = True
    
    st.markdown('#')
 
   
def Cancel():
    st.session_state['ffbrefprice_Status'] = ''
    st.session_state['ffbrefprice_btnNew_disabled'] = False
    st.session_state['ffbrefprice_btnEdit_disabled'] = False
    st.session_state['ffbrefprice_btnDelete_disabled'] = False
    st.session_state['ffbrefprice_btnCancel_disabled'] = True
    st.session_state['ffbrefprice_btnSubmit_disabled'] = True
    
    st.session_state['ffbrefprice_Date_disabled'] = True
    
    ControlNotAllowEdit()


def to_excel(df) -> bytes:
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Sheet1")
    writer.close()
    processed_data = output.getvalue()
    return processed_data


def show_MainPage():
    with placeholder.container():
        # Create an anchor point at here
        st.markdown('<a name="top"></a>', unsafe_allow_html=True)
        
        col1_1, col1_2, col1_3, col1_4 = st.columns([50, 20, 20, 10]) # Mill, From Date, To Date
        col2_1, col2_2 = st.columns([85, 15]) # Scroll links, Export to Excel
        col3_1, col3_2, col3_3 = st.columns([1, 98, 1]) # Grid
        
        st.markdown("---")
               
        
        ############################################
        # Mill, From Date, To Date, Refresh Record #
        ############################################
        with st.container():
            with col1_1:
                ou = st.selectbox(
                                'Mill: ',
                                ('LIBO SAWIT PERKASA PALM OIL MILL',
                                    'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
                                    'SEMUNAI SAWIT PERKASA PALM OIL MILL 2')
                                )

                get_OUKey(ou)
                
            with col1_2:
                st.session_state['ffbrefprice_FromDate'] = st.date_input('From Date', value=st.session_state['ffbrefprice_FromDate'], format="DD/MM/YYYY")
            
            with col1_3:
                st.session_state['ffbrefprice_ToDate'] = st.date_input('To Date', value=st.session_state['ffbrefprice_ToDate'], format="DD/MM/YYYY")
                
            with col1_4:
                st.markdown('####')
                st.button('Refresh',
                        on_click=Call_DisplayGridRecords,
                        args=(st.session_state['ffbrefprice_OUKey'], st.session_state['ffbrefprice_FromDate'], st.session_state['ffbrefprice_ToDate']),
                        help='Click to refresh grid records.',
                        use_container_width=True)

        # Scroll links, Export to Excel
        with st.container():
            with col2_1:
                st.markdown('[Scroll to Pricing](#pricing) | [Scroll to Calculation](#calculation)')
            with col2_2:
                if len(st.session_state['ffbrefprice_RecordList']) != 0:
                    st.download_button(
                        "Download as excel",
                        data=to_excel(pd.DataFrame(st.session_state['ffbrefprice_RecordList']).set_index('Date')),
                        file_name="FFB Reference Price.xlsx",
                        mime="application/vnd.ms-excel",
                        use_container_width=True
                    )
                else:
                    st.markdown('#')

        #####################
        # Grid with Records #
        #####################
        with st.container():
            with col3_2:
                # Configure grid options using GridOptionsBuilder
                if len(st.session_state['ffbrefprice_RecordList']) != 0:
                    builder = GridOptionsBuilder.from_dataframe(st.session_state['ffbrefprice_RecordList'])
                
                    builder.configure_pagination(enabled=False)
                    builder.configure_selection(selection_mode='single', use_checkbox=False)
                    # builder.configure_grid_options(
                    #     pivotMode=True
                    # )
                    builder.configure_default_column(
                        resizable=True,
                        filterable=True,
                        sortable=True,
                        editable=False
                    )
                    builder.configure_column(
                        field='Date',
                        header_name='Date',
                        pinned='left',
                        #width=200,
                        # type=["numericColumn"],
                        # valueFormatter="value.toLocaleString()",
                        # rowGroup=True,
                        # aggFunc="sum" # this tells the grid we'll be summing values on the same reference date
                        # pivot=True,
                        # tooltipField='powerplant',
                        valueFormatter="value != undefined ? new Date(value).toLocaleString('en-GB', {dateStyle:'short'}): ''"
                    )
                    builder.configure_column(
                        field='CPO Tender Price',
                        header_name='CPO Tender Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Selling Price',
                        header_name='CPO Selling Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Production Charges',
                        header_name='CPO Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual CPO Production Charges',
                        header_name='Actual CPO Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Transport Charges',
                        header_name='CPO Transport Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='OER (%)',
                        header_name='OER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Tender Price',
                        header_name='PK Tender Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Selling Price',
                        header_name='PK Selling Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Production Charges',
                        header_name='PK Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual PK Production Charges',
                        header_name='Actual PK Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Transport Charges',
                        header_name='PK Transport Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='KER (%)',
                        header_name='KER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Tender Price',
                        header_name='Shell Tender Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Selling Price',
                        header_name='Shell Selling Price',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Production Charges',
                        header_name='Shell Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual Shell Production Charges',
                        header_name='Actual Shell Production Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Transport Charges',
                        header_name='Shell Transport Charges',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='SER (%)',
                        header_name='SER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO - PPN (Excl. PPN)',
                        header_name='CPO - PPN (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Production Charges (Excl. PPN)',
                        header_name='CPO Production Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Transport Charges (Excl. PPN)',
                        header_name='CPO Transport Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Excl. PPN)',
                        header_name='FFB Price (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK - PPN (Excl. PPN)',
                        header_name='PK - PPN (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Production Charges (Excl. PPN)',
                        header_name='PK Production Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Transport Charges (Excl. PPN)',
                        header_name='PK Transport Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Excl. PPN)',
                        header_name='FFB Price (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell - PPN (Excl. PPN)',
                        header_name='Shell - PPN (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Production Charges (Excl. PPN)',
                        header_name='Shell Production Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Transport Charges (Excl. PPN)',
                        header_name='Shell Transport Charges (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Excl. PPN)',
                        header_name='FFB Price (Excl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO - PPN (Incl. PPN)',
                        header_name='CPO - PPN (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Production Charges (Incl. PPN)',
                        header_name='CPO Production Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Transport Charges (Incl. PPN)',
                        header_name='CPO Transport Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Incl. PPN)',
                        header_name='FFB Price (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK - PPN (Incl. PPN)',
                        header_name='PK - PPN (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Production Charges (Incl. PPN)',
                        header_name='PK Production Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Transport Charges (Incl. PPN)',
                        header_name='PK Transport Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Incl. PPN)',
                        header_name='FFB Price (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell - PPN (Incl. PPN)',
                        header_name='Shell - PPN (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Production Charges (Incl. PPN)',
                        header_name='Shell Production Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Transport Charges (Incl. PPN)',
                        header_name='Shell Transport Charges (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (Incl. PPN)',
                        header_name='FFB Price (Incl. PPN)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO - PPN (FFB Price/kg)',
                        header_name='CPO - PPN (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Production Charges (FFB Price/kg)',
                        header_name='CPO Production Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='CPO Transport Charges (FFB Price/kg)',
                        header_name='CPO Transport Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (FFB Price/kg)',
                        header_name='FFB Price (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK - PPN (FFB Price/kg)',
                        header_name='PK - PPN (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Production Charges (FFB Price/kg)',
                        header_name='PK Production Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='PK Transport Charges (FFB Price/kg)',
                        header_name='PK Transport Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (FFB Price/kg)',
                        header_name='FFB Price (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell - PPN (FFB Price/kg)',
                        header_name='Shell - PPN (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Production Charges (FFB Price/kg)',
                        header_name='Shell Production Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Shell Transport Charges (FFB Price/kg)',
                        header_name='Shell Transport Charges (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='FFB Price (FFB Price/kg)',
                        header_name='FFB Price (FFB Price/kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    grid_options = builder.build()

                    # Display AgGrid
                    ag = AgGrid(st.session_state['ffbrefprice_RecordList'],
                                gridOptions=grid_options,
                                editable=False,
                                allow_unsafe_jscode=True,
                                theme='balham',
                                height=500,
                                #fit_columns_on_grid_load=True,
                                reload_data=False,
                                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                custom_css={
                                    '#gridToolBar': {
                                        'padding-bottom': '0px !important'
                                    }
                                })
                    
                else:
                    testFrame=pd.DataFrame({"col1":[np.nan],"col2":[np.nan]})
                    ag = AgGrid(testFrame,
                                editable=False,
                                allow_unsafe_jscode=True,
                                theme='balham',
                                height=500,
                                #fit_columns_on_grid_load=True,
                                reload_data=False,
                                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                custom_css={
                                    '#gridToolBar': {
                                        'padding-bottom': '0px !important'
                                    }
                                })
        
        
        # Tabs
        tab1, tab2 = st.tabs(['Calculation', 'FFB Reference Price'])
        
        with tab1:
            col4_1, col4_2, col4_3, col4_4, col4_5, col4_6, col4_7= st.columns([25, 25, 10, 10, 10, 10, 10]) # Mill and Date
            
            # Create an anchor point at here
            st.markdown('<a name="pricing"></a>', unsafe_allow_html=True)
            
            st.info('##### Pricing')
            st.markdown('[Scroll to Calculation](#calculation) | [Scroll to Top](#top)')
            st.markdown('###### CPO Pricing (Include PPN)')
            col5_1, col5_2, col5_3, col5_4, col5_5, col5_6, col5_7, col5_8, col5_9, col5_10, col5_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # CPO Pricing
            
            st.markdown('###### PK Pricing (Exclude PPN)')
            col6_1, col6_2, col6_3, col6_4, col6_5, col6_6, col6_7, col6_8, col6_9, col6_10, col6_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # PK Pricing
            
            st.markdown('###### Shell Pricing (Exclude PPN)')
            col7_1, col7_2, col7_3, col7_4, col7_5, col7_6, col7_7, col7_8, col7_9, col7_10, col7_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # Shell Pricing
            
            st.markdown('#####')
            st.success('##### Calculation')
            
            # Calculation for FFB Price (Exclude PPN), FFB Price (Include PPN) & FFB Price/kg (Actual Production)
            # FFB Price (Exclude PPN)
            st.markdown('###### FFB Price (Exclude PPN)')
            col8_1, col8_2, col8_3, col8_4, col8_5, col8_6, col8_7, col8_8, col8_9, col8_10, col8_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # CPO Price (Exclude PPN)
            col9_1, col9_2, col9_3, col9_4, col9_5, col9_6, col9_7, col9_8, col9_9, col9_10, col9_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # PK Price (Exclude PPN)
            col10_1, col10_2, col10_3, col10_4, col10_5, col10_6, col10_7, col10_8, col10_9, col10_10, col10_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # Shell Price (Exclude PPN)
            
            st.markdown('#####')
            
            # FFB Price (Include PPN)
            st.markdown('###### FFB Price (Include PPN)')
            col11_1, col11_2, col11_3, col11_4, col11_5, col11_6, col11_7, col11_8, col11_9, col11_10, col11_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # CPO Price (Include PPN)
            col12_1, col12_2, col12_3, col12_4, col12_5, col12_6, col12_7, col12_8, col12_9, col12_10, col12_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # PK Price (Include PPN)
            col13_1, col13_2, col13_3, col13_4, col13_5, col13_6, col13_7, col13_8, col13_9, col13_10, col13_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # Shell Price (Include PPN)
            
            st.markdown('#####')
            
            # FFB Price/kg (Actual Production)
            st.markdown('###### FFB Price/kg (Actual Production)')
            col14_1, col14_2, col14_3, col14_4, col14_5, col14_6, col14_7, col14_8, col14_9, col14_10, col14_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # CPO Price (Actual Production)
            col15_1, col15_2, col15_3, col15_4, col15_5, col15_6, col15_7, col15_8, col15_9, col15_10, col15_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # PK Price (Actual Production)
            col16_1, col16_2, col16_3, col16_4, col16_5, col16_6, col16_7, col16_8, col16_9, col16_10, col16_11 = st.columns([15, 2, 15, 2, 15, 2, 15, 2, 15, 2, 15]) # Shell Price (Actual Production)
            
           
            
        
        
            st.markdown('[Scroll to Pricing](#pricing) | [Scroll to Top](#top)')
            
            # Define the style of the Number Fields and Text Fields
            st.markdown("""
                        <style>
                        .st-emotion-cache-q8sbsg p {
                            color: white;
                        }
                        .stNumberInput [data-baseweb=base-input] {
                            background-color: white;
                            -webkit-text-fill-color: Black;
                        }
                        .stTextInput [data-baseweb=base-input] {
                            background-color: white;
                            -webkit-text-fill-color: Black;
                        }

                        .stNumberInput [data-baseweb=base-input] [disabled=""]{
                            background-color: rgb(64, 64, 64);
                            -webkit-text-fill-color: white;
                        }
                        .stTextInput [data-baseweb=base-input] [disabled=""]{
                            background-color: rgb(64, 64, 64);
                            -webkit-text-fill-color: white;
                        }
                        
                        .stTabs [data-baseweb="tab-list"] {
                            gap: 5px;
                        }

                        .stTabs [data-baseweb="tab"] {
                            height: 30px;
                            white-space: pre-wrap;
                            background-color: rgb(171, 178, 185);
                            border-radius: 4px 4px 0px 0px;
                            gap: 1px;
                            padding-top: 10px;
                            padding-bottom: 10px;
                            padding-left: 10px;
                            padding-right: 10px;
                            color: black;
                        }
                        
                        .stTabs [aria-selected="true"] {
                            background-color: rgb(230, 126, 34);
                        }
                        </style>
                        """, unsafe_allow_html=True)
            
            
            ######################################################
            # Mill, Date, New Record, Edit Record, Submit Record #
            ######################################################
            with st.container():
                with col4_1:
                    st.session_state['ffbrefprice_Mill'] = ou
                    
                    st.selectbox('Mill', options=('LIBO SAWIT PERKASA PALM OIL MILL',
                                                'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
                                                'SEMUNAI SAWIT PERKASA PALM OIL MILL 2'),  
                                key='ffbrefprice_Mill', disabled=True)

                    get_OUKey(st.session_state['ffbrefprice_Mill'])
                    
                with col4_2:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_Date'] = datetime.strptime(ag['selected_rows'][0]['Date'], "%Y-%m-%dT%H:%M:%S") if len(ag['selected_rows']) == 1 else datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S") # datetime.strptime('1900-01-01T00:00:00', "%Y-%m-%dT%H:%M:%S")
                    st.date_input('Date', key='ffbrefprice_Date', disabled=st.session_state['ffbrefprice_Date_disabled'], format="DD/MM/YYYY")
                    
                with col4_3:
                    st.markdown('#')
                    st.button('New Record',
                            on_click=New,
                            args=(),
                            help='Click to add new record.',
                            disabled=st.session_state['ffbrefprice_btnNew_disabled'],
                            use_container_width=True)
                with col4_4:
                    st.markdown('#')
                    st.button('Edit Record',
                            on_click=Edit,
                            args=(),
                            help='Click to edit record.',
                            disabled=st.session_state['ffbrefprice_btnEdit_disabled'],
                            use_container_width=True)
                with col4_5:
                    st.markdown('#')
                    st.button('Delete',
                            on_click=Delete,
                            args=(st.session_state['ffbrefprice_Date'], st.session_state['ffbrefprice_OUKey']),
                            help='Click to delete this record.',
                            disabled=st.session_state['ffbrefprice_btnDelete_disabled'],
                            use_container_width=True)
                with col4_6:
                    st.markdown('#')
                    st.button('Cancel',
                            on_click=Cancel,
                            args=(),
                            help='Click to cancel add or edit record.',
                            disabled=st.session_state['ffbrefprice_btnCancel_disabled'],
                            use_container_width=True)
                with col4_7:
                    st.markdown('#')
                    st.button('Submit',
                            on_click=Submit,
                            args=(st.session_state['ffbrefprice_Date'], st.session_state['ffbrefprice_OUKey'], 
                                  st.session_state['ffbrefprice_CPOTdPrice'], st.session_state['ffbrefprice_CPOSellPrice'], st.session_state['ffbrefprice_CPOProCharges'], st.session_state['ffbrefprice_CPORealProCharges'], st.session_state['ffbrefprice_CPOTransCharges'], st.session_state['ffbrefprice_RendCPO'],
                                  st.session_state['ffbrefprice_PKTdPrice'], st.session_state['ffbrefprice_PKSellPrice'], st.session_state['ffbrefprice_PKProCharges'], st.session_state['ffbrefprice_PKRealProCharges'], st.session_state['ffbrefprice_PKTransCharges'], st.session_state['ffbrefprice_RendPK'],
                                  st.session_state['ffbrefprice_ShellTdPrice'], st.session_state['ffbrefprice_ShellSellPrice'], st.session_state['ffbrefprice_ShellProCharges'], st.session_state['ffbrefprice_ShellRealProCharges'], st.session_state['ffbrefprice_ShellTransCharges'], st.session_state['ffbrefprice_RendShell'],
                                  st.session_state['ffbrefprice_ETaxCPO'], st.session_state['ffbrefprice_ETaxCPOProCharges'], st.session_state['ffbrefprice_ETaxCPOTransCharges'], st.session_state['ffbrefprice_ETaxCPOPrice'],
                                  st.session_state['ffbrefprice_ETaxPK'], st.session_state['ffbrefprice_ETaxPKProCharges'], st.session_state['ffbrefprice_ETaxPKTransCharges'], st.session_state['ffbrefprice_ETaxPKPrice'],
                                  st.session_state['ffbrefprice_ETaxShell'], st.session_state['ffbrefprice_ETaxShellProCharges'], st.session_state['ffbrefprice_ETaxShellTransCharges'], st.session_state['ffbrefprice_ETaxShellPrice'],
                                  st.session_state['ffbrefprice_ITaxCPO'], st.session_state['ffbrefprice_ITaxCPOProCharges'], st.session_state['ffbrefprice_ITaxCPOTransCharges'], st.session_state['ffbrefprice_ITaxCPOPrice'],
                                  st.session_state['ffbrefprice_ITaxPK'], st.session_state['ffbrefprice_ITaxPKProCharges'], st.session_state['ffbrefprice_ITaxPKTransCharges'], st.session_state['ffbrefprice_ITaxPKPrice'],
                                  st.session_state['ffbrefprice_ITaxShell'], st.session_state['ffbrefprice_ITaxShellProCharges'], st.session_state['ffbrefprice_ITaxShellTransCharges'], st.session_state['ffbrefprice_ITaxShellPrice'],
                                  st.session_state['ffbrefprice_RTaxCPO'], st.session_state['ffbrefprice_RCPOProCharges'], st.session_state['ffbrefprice_RCPOTransCharges'], st.session_state['ffbrefprice_RCPOPrice'],
                                  st.session_state['ffbrefprice_RTaxPK'], st.session_state['ffbrefprice_RPKProCharges'], st.session_state['ffbrefprice_RPKTransCharges'], st.session_state['ffbrefprice_RPKPrice'],
                                  st.session_state['ffbrefprice_RTaxShell'], st.session_state['ffbrefprice_RShellProCharges'], st.session_state['ffbrefprice_RShellTransCharges'], st.session_state['ffbrefprice_RShellPrice']), 
                            help='Click to submit record.',
                            disabled=st.session_state['ffbrefprice_btnSubmit_disabled'],
                            use_container_width=True)
            
                
            
            #############################
            # CPO, PK and Shell Pricing #
            #############################
            # CPO Pricing
            with st.container():
                with col5_1:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_CPOTdPrice'] = float(ag['selected_rows'][0]['CPO Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_CPOTdPrice']
                    st.number_input('CPO Tender Price', key='ffbrefprice_CPOTdPrice', disabled=st.session_state['ffbrefprice_CPOTdPrice_disabled'])
                with col5_2:
                    st.markdown('###')
                    st.markdown('###')
                with col5_3:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_CPOSellPrice'] = float(ag['selected_rows'][0]['CPO Selling Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_CPOSellPrice']
                    st.number_input('CPO Selling Price', key='ffbrefprice_CPOSellPrice', disabled=st.session_state['ffbrefprice_CPOSellPrice_disabled'])
                with col5_4:
                    st.markdown('###')
                    st.markdown('###')
                with col5_5:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_CPOProCharges'] = float(ag['selected_rows'][0]['CPO Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_CPOProCharges']
                    st.number_input('CPO Production Charges', key='ffbrefprice_CPOProCharges', disabled=st.session_state['ffbrefprice_CPOProCharges_disabled'])
                with col5_6:
                    st.markdown('###')
                    st.markdown('###')
                with col5_7:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_CPORealProCharges'] = float(ag['selected_rows'][0]['Actual CPO Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_CPORealProCharges']
                    st.number_input('Act. CPO Production Charges', key='ffbrefprice_CPORealProCharges', disabled=st.session_state['ffbrefprice_CPORealProCharges_disabled'])
                with col5_8:
                    st.markdown('###')
                    st.markdown('###')
                with col5_9:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_CPOTransCharges'] = float(ag['selected_rows'][0]['CPO Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_CPOTransCharges']
                    st.number_input('CPO Transport Charges', key='ffbrefprice_CPOTransCharges', disabled=st.session_state['ffbrefprice_CPOTransCharges_disabled'])
                with col5_10:
                    st.markdown('###')
                    st.markdown('###')
                with col5_11:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_RendCPO'] = float(ag['selected_rows'][0]['OER (%)']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_RendCPO']
                    st.number_input('OER (%)', key='ffbrefprice_RendCPO', disabled=st.session_state['ffbrefprice_RendCPO_disabled'])
                
        
            # PK Pricing
            with st.container():
                with col6_1:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_PKTdPrice'] = float(ag['selected_rows'][0]['PK Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_PKTdPrice']
                    st.number_input('PK Tender Price', key='ffbrefprice_PKTdPrice', disabled=st.session_state['ffbrefprice_PKTdPrice_disabled'])
                with col6_2:
                    st.markdown('###')
                    st.markdown('###')
                with col6_3:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_PKSellPrice'] = float(ag['selected_rows'][0]['PK Selling Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_PKSellPrice']
                    st.number_input('PK Selling Price', key='ffbrefprice_PKSellPrice', disabled=st.session_state['ffbrefprice_PKSellPrice_disabled'])
                with col6_4:
                    st.markdown('###')
                    st.markdown('###')
                with col6_5:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_PKProCharges'] = float(ag['selected_rows'][0]['PK Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_PKProCharges']
                    st.number_input('PK Production Charges', key='ffbrefprice_PKProCharges', disabled=st.session_state['ffbrefprice_PKProCharges_disabled'])
                with col6_6:
                    st.markdown('###')
                    st.markdown('###')
                with col6_7:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_PKRealProCharges'] = float(ag['selected_rows'][0]['Actual PK Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_PKRealProCharges']
                    st.number_input('Act. PK Production Charges', key='ffbrefprice_PKRealProCharges', disabled=st.session_state['ffbrefprice_PKRealProCharges_disabled'])
                with col6_8:
                    st.markdown('###')
                    st.markdown('###')
                with col6_9:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_PKTransCharges'] = float(ag['selected_rows'][0]['PK Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_PKTransCharges']
                    st.number_input('PK Transport Charges', key='ffbrefprice_PKTransCharges', disabled=st.session_state['ffbrefprice_PKTransCharges_disabled'])
                with col6_10:
                    st.markdown('###')
                    st.markdown('###')
                with col6_11:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_RendPK'] = float(ag['selected_rows'][0]['KER (%)']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_RendPK']
                    st.number_input('KER (%)', key='ffbrefprice_RendPK', disabled=st.session_state['ffbrefprice_RendPK_disabled'])
                
                
            # Shell Pricing
            with st.container():
                with col7_1:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_ShellTdPrice'] = float(ag['selected_rows'][0]['Shell Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_ShellTdPrice']
                    st.number_input('Shell Tender Price', key='ffbrefprice_ShellTdPrice', disabled=st.session_state['ffbrefprice_ShellTdPrice_disabled'])
                with col7_2:
                    st.markdown('###')
                    st.markdown('###')
                with col7_3:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_ShellSellPrice'] = float(ag['selected_rows'][0]['Shell Selling Price']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_ShellSellPrice']
                    st.number_input('Shell Selling Price', key='ffbrefprice_ShellSellPrice', disabled=st.session_state['ffbrefprice_ShellSellPrice_disabled'])
                with col7_4:
                    st.markdown('###')
                    st.markdown('###')
                with col7_5:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_ShellProCharges'] = float(ag['selected_rows'][0]['Shell Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_ShellProCharges']
                    st.number_input('Shell Production Charges', key='ffbrefprice_ShellProCharges', disabled=st.session_state['ffbrefprice_ShellProCharges_disabled'])
                with col7_6:
                    st.markdown('###')
                    st.markdown('###')
                with col7_7:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_ShellRealProCharges'] = float(ag['selected_rows'][0]['Actual Shell Production Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_ShellRealProCharges']
                    st.number_input('Act. Shell Production Charges', key='ffbrefprice_ShellRealProCharges', disabled=st.session_state['ffbrefprice_ShellRealProCharges_disabled'])
                with col7_8:
                    st.markdown('###')
                    st.markdown('###')
                with col7_9:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_ShellTransCharges'] = float(ag['selected_rows'][0]['Shell Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_ShellTransCharges']
                    st.number_input('Shell Transport Charges', key='ffbrefprice_ShellTransCharges', disabled=st.session_state['ffbrefprice_ShellTransCharges_disabled'])
                with col7_10:
                    st.markdown('###')
                    st.markdown('###')
                with col7_11:
                    if st.session_state['ffbrefprice_Status'] == '':
                        st.session_state['ffbrefprice_RendShell'] = float(ag['selected_rows'][0]['SER (%)']) if len(ag['selected_rows']) == 1 else st.session_state['ffbrefprice_RendShell']
                    st.number_input('SER (%)', key='ffbrefprice_RendShell', disabled=st.session_state['ffbrefprice_RendShell_disabled'])
                    
                        
            
            
            ###############
            # Calculation #
            ###############
            # CPO Price (Exclude PPN)
            with st.container():
                with col8_1:
                    st.session_state['ffbrefprice_ETaxCPOTdPrice'] = st.session_state['ffbrefprice_CPOTdPrice']
                    st.number_input('CPO Selling Price', key='ffbrefprice_ETaxCPOTdPrice', disabled=True)
                with col8_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col8_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxCPO'] = float(ag['selected_rows'][0]['CPO - PPN (Excl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ETaxCPO', disabled=st.session_state['ffbrefprice_ETaxCPO_disabled'], format='%0.2f')  
                with col8_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col8_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxCPOProCharges'] = float(ag['selected_rows'][0]['CPO Production Charges (Excl. PPN)'])
                    st.number_input('CPO Production Charges', key='ffbrefprice_ETaxCPOProCharges', disabled=st.session_state['ffbrefprice_ETaxCPOProCharges_disabled']) 
                with col8_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col8_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxCPOTransCharges'] = float(ag['selected_rows'][0]['CPO Transport Charges (Excl. PPN)'])
                    st.number_input('CPO Transport Charges', key='ffbrefprice_ETaxCPOTransCharges', disabled=st.session_state['ffbrefprice_ETaxCPOTransCharges_disabled'])
                with col8_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col8_9:
                    st.session_state['ffbrefprice_ETaxRendCPO'] = st.session_state['ffbrefprice_RendCPO']
                    st.number_input('OER (%)', key='ffbrefprice_ETaxRendCPO', disabled=True, format='%0.2f') 
                with col8_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col8_11:
                    st.session_state['ffbrefprice_ETaxCPOPrice'] = format(float(((st.session_state['ffbrefprice_CPOTdPrice'] / st.session_state['ffbrefprice_ETaxCPO'] if  st.session_state['ffbrefprice_ETaxCPO'] > 0 else 0) - st.session_state['ffbrefprice_ETaxCPOProCharges'] - st.session_state['ffbrefprice_ETaxCPOTransCharges']) * (st.session_state['ffbrefprice_RendCPO'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ETaxCPOPrice', disabled=True)
            
            # PK Price (Exclude PPN)
            with st.container():
                with col9_1:
                    st.session_state['ffbrefprice_ETaxPKTdPrice'] = st.session_state['ffbrefprice_PKTdPrice']
                    st.number_input('PK Selling Price', key='ffbrefprice_ETaxPKTdPrice', disabled=True)
                with col9_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col9_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxPK'] = float(ag['selected_rows'][0]['PK - PPN (Excl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ETaxPK', disabled=st.session_state['ffbrefprice_ETaxPK_disabled'], format='%0.2f')  
                with col9_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col9_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxPKProCharges'] = float(ag['selected_rows'][0]['PK Production Charges (Excl. PPN)'])
                    st.number_input('PK Production Charges', key='ffbrefprice_ETaxPKProCharges', disabled=st.session_state['ffbrefprice_ETaxPKProCharges_disabled']) 
                with col9_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col9_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxPKTransCharges'] = float(ag['selected_rows'][0]['PK Transport Charges (Excl. PPN)'])
                    st.number_input('PK Transport Charges', key='ffbrefprice_ETaxPKTransCharges', disabled=st.session_state['ffbrefprice_ETaxPKTransCharges_disabled'])
                with col9_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col9_9:
                    st.session_state['ffbrefprice_ETaxRendPK'] = st.session_state['ffbrefprice_RendPK']
                    st.number_input('KER (%)', key='ffbrefprice_ETaxRendPK', disabled=True, format='%0.2f') 
                with col9_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col9_11:
                    st.session_state['ffbrefprice_ETaxPKPrice'] = format(float(((st.session_state['ffbrefprice_PKTdPrice'] / st.session_state['ffbrefprice_ETaxPK'] if  st.session_state['ffbrefprice_ETaxPK'] > 0 else 0) - st.session_state['ffbrefprice_ETaxPKProCharges'] - st.session_state['ffbrefprice_ETaxPKTransCharges']) * (st.session_state['ffbrefprice_RendPK'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ETaxPKPrice', disabled=True)
                
            # Shell Price (Exclude PPN)
            with st.container():
                with col10_1:
                    st.session_state['ffbrefprice_ETaxShellTdPrice'] = st.session_state['ffbrefprice_ShellTdPrice']
                    st.number_input('Shell Selling Price', key='ffbrefprice_ETaxShellTdPrice', disabled=True)
                with col10_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col10_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxShell'] = float(ag['selected_rows'][0]['Shell - PPN (Excl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ETaxShell', disabled=st.session_state['ffbrefprice_ETaxShell_disabled'], format='%0.2f')  
                with col10_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col10_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxShellProCharges'] = float(ag['selected_rows'][0]['Shell Production Charges (Excl. PPN)'])
                    st.number_input('Shell Production Charges', key='ffbrefprice_ETaxShellProCharges', disabled=st.session_state['ffbrefprice_ETaxShellProCharges_disabled']) 
                with col10_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col10_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ETaxShellTransCharges'] = float(ag['selected_rows'][0]['Shell Transport Charges (Excl. PPN)'])
                    st.number_input('Shell Transport Charges', key='ffbrefprice_ETaxShellTransCharges', disabled=st.session_state['ffbrefprice_ETaxShellTransCharges_disabled'])
                with col10_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col10_9:
                    st.session_state['ffbrefprice_ETaxRendShell'] = st.session_state['ffbrefprice_RendShell']
                    st.number_input('SER (%)', key='ffbrefprice_ETaxRendShell', disabled=True, format='%0.2f') 
                with col10_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col10_11:
                    st.session_state['ffbrefprice_ETaxShellPrice'] = format(float(((st.session_state['ffbrefprice_ShellTdPrice'] / st.session_state['ffbrefprice_ETaxShell'] if  st.session_state['ffbrefprice_ETaxShell'] > 0 else 0) - st.session_state['ffbrefprice_ETaxShellProCharges'] - st.session_state['ffbrefprice_ETaxShellTransCharges']) * (st.session_state['ffbrefprice_RendShell'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ETaxShellPrice', disabled=True)   
            
            
            # CPO Price (Include PPN)
            with st.container():
                with col11_1:
                    st.session_state['ffbrefprice_ITaxCPOTdPrice'] = st.session_state['ffbrefprice_CPOTdPrice']
                    st.number_input('CPO Selling Price', key='ffbrefprice_ITaxCPOTdPrice', disabled=True)
                with col11_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col11_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxCPO'] = float(ag['selected_rows'][0]['CPO - PPN (Incl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ITaxCPO', disabled=st.session_state['ffbrefprice_ITaxCPO_disabled'], format='%0.2f')  
                with col11_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col11_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxCPOProCharges'] = float(ag['selected_rows'][0]['CPO Production Charges (Incl. PPN)'])
                    st.number_input('CPO Production Charges', key='ffbrefprice_ITaxCPOProCharges', disabled=st.session_state['ffbrefprice_ITaxCPOProCharges_disabled']) 
                with col11_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col11_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxCPOTransCharges'] = float(ag['selected_rows'][0]['CPO Transport Charges (Incl. PPN)'])
                    st.number_input('CPO Transport Charges', key='ffbrefprice_ITaxCPOTransCharges', disabled=st.session_state['ffbrefprice_ITaxCPOTransCharges_disabled'])
                with col11_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col11_9:
                    st.session_state['ffbrefprice_ITaxRendCPO'] = st.session_state['ffbrefprice_RendCPO']
                    st.number_input('OER (%)', key='ffbrefprice_ITaxRendCPO', disabled=True, format='%0.2f') 
                with col11_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col11_11:
                    st.session_state['ffbrefprice_ITaxCPOPrice'] = format(float(((st.session_state['ffbrefprice_CPOTdPrice'] / st.session_state['ffbrefprice_ITaxCPO'] if  st.session_state['ffbrefprice_ITaxCPO'] > 0 else 0) - st.session_state['ffbrefprice_ITaxCPOProCharges'] - st.session_state['ffbrefprice_ITaxCPOTransCharges']) * (st.session_state['ffbrefprice_RendCPO'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ITaxCPOPrice', disabled=True)
        

            # PK Price (Include PPN)
            with st.container():
                with col12_1:
                    st.session_state['ffbrefprice_ITaxPKTdPrice'] = st.session_state['ffbrefprice_PKTdPrice']
                    st.number_input('PK Selling Price', key='ffbrefprice_ITaxPKTdPrice', disabled=True)
                with col12_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col12_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxPK'] = float(ag['selected_rows'][0]['PK - PPN (Incl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ITaxPK', disabled=st.session_state['ffbrefprice_ITaxPK_disabled'], format='%0.2f')  
                with col12_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col12_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxPKProCharges'] = float(ag['selected_rows'][0]['PK Production Charges (Incl. PPN)'])
                    st.number_input('PK Production Charges', key='ffbrefprice_ITaxPKProCharges', disabled=st.session_state['ffbrefprice_ITaxPKProCharges_disabled']) 
                with col12_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col12_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxPKTransCharges'] = float(ag['selected_rows'][0]['PK Transport Charges (Incl. PPN)'])
                    st.number_input('PK Transport Charges', key='ffbrefprice_ITaxPKTransCharges', disabled=st.session_state['ffbrefprice_ITaxPKTransCharges_disabled'])
                with col12_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col12_9:
                    st.session_state['ffbrefprice_ITaxRendPK'] = st.session_state['ffbrefprice_RendPK']
                    st.number_input('KER (%)', key='ffbrefprice_ITaxRendPK', disabled=True, format='%0.2f') 
                with col12_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col12_11:
                    st.session_state['ffbrefprice_ITaxPKPrice'] = format(float(((st.session_state['ffbrefprice_PKTdPrice'] / st.session_state['ffbrefprice_ITaxPK'] if  st.session_state['ffbrefprice_ITaxPK'] > 0 else 0) - st.session_state['ffbrefprice_ITaxPKProCharges'] - st.session_state['ffbrefprice_ITaxPKTransCharges']) * (st.session_state['ffbrefprice_RendPK'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ITaxPKPrice', disabled=True)
            

            # Shell Price (Include PPN)
            with st.container():
                with col13_1:
                    st.session_state['ffbrefprice_ITaxShellTdPrice'] = st.session_state['ffbrefprice_ShellTdPrice']
                    st.number_input('Shell Selling Price', key='ffbrefprice_ITaxShellTdPrice', disabled=True)
                with col13_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col13_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxShell'] = float(ag['selected_rows'][0]['Shell - PPN (Incl. PPN)'])
                    st.number_input('PPN (%)', key='ffbrefprice_ITaxShell', disabled=st.session_state['ffbrefprice_ITaxShell_disabled'], format='%0.2f')  
                with col13_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col13_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxShellProCharges'] = float(ag['selected_rows'][0]['Shell Production Charges (Incl. PPN)'])
                    st.number_input('Shell Production Charges', key='ffbrefprice_ITaxShellProCharges', disabled=st.session_state['ffbrefprice_ITaxShellProCharges_disabled']) 
                with col13_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col13_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_ITaxShellTransCharges'] = float(ag['selected_rows'][0]['Shell Transport Charges (Incl. PPN)'])
                    st.number_input('Shell Transport Charges', key='ffbrefprice_ITaxShellTransCharges', disabled=st.session_state['ffbrefprice_ITaxShellTransCharges_disabled'])
                with col13_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col13_9:
                    st.session_state['ffbrefprice_ITaxRendShell'] = st.session_state['ffbrefprice_RendShell']
                    st.number_input('SER (%)', key='ffbrefprice_ITaxRendShell', disabled=True, format='%0.2f') 
                with col13_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col13_11:
                    st.session_state['ffbrefprice_ITaxShellPrice'] = format(float(((st.session_state['ffbrefprice_ShellTdPrice'] / st.session_state['ffbrefprice_ITaxShell'] if  st.session_state['ffbrefprice_ITaxShell'] > 0 else 0) - st.session_state['ffbrefprice_ITaxShellProCharges'] - st.session_state['ffbrefprice_ITaxShellTransCharges']) * (st.session_state['ffbrefprice_RendShell'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_ITaxShellPrice', disabled=True)  
        

            # CPO Price (Actual Production)
            with st.container():
                with col14_1:
                    st.session_state['ffbrefprice_RCPOTdPrice'] = st.session_state['ffbrefprice_CPOTdPrice']
                    st.number_input('CPO Selling Price', key='ffbrefprice_RCPOTdPrice', disabled=True)
                with col14_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col14_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RTaxCPO'] = float(ag['selected_rows'][0]['CPO - PPN (FFB Price/kg)'])
                    st.number_input('PPN (%)', key='ffbrefprice_RTaxCPO', disabled=st.session_state['ffbrefprice_RTaxCPO_disabled'], format='%0.2f')  
                with col14_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col14_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RCPOProCharges'] = float(ag['selected_rows'][0]['CPO Production Charges (FFB Price/kg)'])
                    st.number_input('CPO Production Charges', key='ffbrefprice_RCPOProCharges', disabled=st.session_state['ffbrefprice_RCPOProCharges_disabled']) 
                with col14_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col14_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RCPOTransCharges'] = float(ag['selected_rows'][0]['CPO Transport Charges (FFB Price/kg)'])
                    st.number_input('CPO Transport Charges', key='ffbrefprice_RCPOTransCharges', disabled=st.session_state['ffbrefprice_RCPOTransCharges_disabled'])
                with col14_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col14_9:
                    st.session_state['ffbrefprice_RRendCPO'] = st.session_state['ffbrefprice_RendCPO']
                    st.number_input('OER (%)', key='ffbrefprice_RRendCPO', disabled=True, format='%0.2f') 
                with col14_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col14_11:
                    st.session_state['ffbrefprice_RCPOPrice'] = format(float(((st.session_state['ffbrefprice_CPOTdPrice'] / st.session_state['ffbrefprice_RTaxCPO'] if  st.session_state['ffbrefprice_RTaxCPO'] > 0 else 0) - st.session_state['ffbrefprice_RCPOProCharges'] - st.session_state['ffbrefprice_RCPOTransCharges']) * (st.session_state['ffbrefprice_RendCPO'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_RCPOPrice', disabled=True)

            # PK Price (Actual Production)
            with st.container():
                with col15_1:
                    st.session_state['ffbrefprice_RPKTdPrice'] = st.session_state['ffbrefprice_PKTdPrice']
                    st.number_input('PK Selling Price', key='ffbrefprice_RPKTdPrice', disabled=True)
                with col15_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col15_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RTaxPK'] = float(ag['selected_rows'][0]['PK - PPN (FFB Price/kg)'])
                    st.number_input('PPN (%)', key='ffbrefprice_RTaxPK', disabled=st.session_state['ffbrefprice_RTaxPK_disabled'], format='%0.2f')  
                with col15_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col15_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RPKProCharges'] = float(ag['selected_rows'][0]['PK Production Charges (FFB Price/kg)'])
                    st.number_input('PK Production Charges', key='ffbrefprice_RPKProCharges', disabled=st.session_state['ffbrefprice_RPKProCharges_disabled']) 
                with col15_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col15_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RPKTransCharges'] = float(ag['selected_rows'][0]['PK Transport Charges (FFB Price/kg)'])
                    st.number_input('PK Transport Charges', key='ffbrefprice_RPKTransCharges', disabled=st.session_state['ffbrefprice_RPKTransCharges_disabled'])
                with col15_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col15_9:
                    st.session_state['ffbrefprice_RRendPK'] = st.session_state['ffbrefprice_RendPK']
                    st.number_input('KER (%)', key='ffbrefprice_RRendPK', disabled=True, format='%0.2f') 
                with col15_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col15_11:
                    st.session_state['ffbrefprice_RPKPrice'] = format(float(((st.session_state['ffbrefprice_PKTdPrice'] / st.session_state['ffbrefprice_RTaxPK'] if  st.session_state['ffbrefprice_RTaxPK'] > 0 else 0) - st.session_state['ffbrefprice_RPKProCharges'] - st.session_state['ffbrefprice_RPKTransCharges']) * (st.session_state['ffbrefprice_RendPK'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_RPKPrice', disabled=True)
                    
            # Shell Price (Actual Production)
            with st.container():
                with col16_1:
                    st.session_state['ffbrefprice_RShellTdPrice'] = st.session_state['ffbrefprice_ShellTdPrice']
                    st.number_input('Shell Selling Price', key='ffbrefprice_RShellTdPrice', disabled=True)
                with col16_2:
                    st.markdown('###')
                    st.markdown('### :')
                with col16_3:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RTaxShell'] = float(ag['selected_rows'][0]['Shell - PPN (FFB Price/kg)'])
                    st.number_input('PPN (%)', key='ffbrefprice_RTaxShell', disabled=st.session_state['ffbrefprice_RTaxShell_disabled'], format='%0.2f')  
                with col16_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col16_5:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RShellProCharges'] = float(ag['selected_rows'][0]['Shell Production Charges (FFB Price/kg)'])
                    st.number_input('Shell Production Charges', key='ffbrefprice_RShellProCharges', disabled=st.session_state['ffbrefprice_RShellProCharges_disabled']) 
                with col16_6:
                    st.markdown('###')
                    st.markdown('### -')
                with col16_7:
                    if st.session_state['ffbrefprice_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['ffbrefprice_RShellTransCharges'] = float(ag['selected_rows'][0]['Shell Transport Charges (FFB Price/kg)'])
                    st.number_input('Shell Transport Charges', key='ffbrefprice_RShellTransCharges', disabled=st.session_state['ffbrefprice_RShellTransCharges_disabled'])
                with col16_8:   
                    st.markdown('###')
                    st.markdown('### x')
                with col16_9:
                    st.session_state['ffbrefprice_RRendShell'] = st.session_state['ffbrefprice_RendShell']
                    st.number_input('SER (%)', key='ffbrefprice_RRendShell', disabled=True, format='%0.2f') 
                with col16_10:
                    st.markdown('###')
                    st.markdown('### =')
                with col16_11:
                    st.session_state['ffbrefprice_RShellPrice'] = format(float(((st.session_state['ffbrefprice_ShellTdPrice'] / st.session_state['ffbrefprice_RTaxShell'] if  st.session_state['ffbrefprice_RTaxShell'] > 0 else 0) - st.session_state['ffbrefprice_RShellProCharges'] - st.session_state['ffbrefprice_RShellTransCharges']) * (st.session_state['ffbrefprice_RendShell'] / 100)), '.2f')
                    st.text_input('FFB Price', key='ffbrefprice_RShellPrice', disabled=True)
        
        
        # FFB Reference Price by OER
        with tab2:
            
            # Export to excel
            col17_1, col17_2 = st.columns([85, 15])
            
            # FFB Reference Price by OER Grid
            col18_1, col18_2, col18_3 = st.columns([1, 98, 1])
            
            
            with st.container():
                with col18_2:
                    # Configure grid options using GridOptionsBuilder
                    if len(st.session_state['ffbrefprice_RecordList']) != 0 and len(ag['selected_rows']) == 1:
                       
                        Call_DisplayFFBPriceRecords(st.session_state['ffbrefprice_OUKey'], st.session_state['ffbrefprice_Date'])
                        
                        if len(st.session_state['ffbrefprice_FFBPriceList']) != 0:
                            builder2 = GridOptionsBuilder.from_dataframe(st.session_state['ffbrefprice_FFBPriceList'])
                            builder2.configure_pagination(enabled=False)
                            # builder2.configure_selection(selection_mode='single', use_checkbox=False)
                            builder2.configure_default_column(
                                resizable=True,
                                filterable=True,
                                sortable=True,
                                editable=False
                            )
                            builder2.configure_column(
                                field='OER (%)',
                                header_name='OER (%)',
                                width=100,
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='FFB Price (Excl. PK & Shell)',
                                header_name='FFB Price (Excl. PK & Shell)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='PK Price',
                                header_name='PK Price',
                                width=100,
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='Shell Price',
                                header_name='Shell Price',
                                width=100,
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='FFB Price/kg (Excl. PPN)',
                                header_name='FFB Price/kg (Excl. PPN)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='FFB Price/kg (Incl. PPN)',
                                header_name='FFB Price/kg (Incl. PPN)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='FFB Price/kg (Actual Production)',
                                width=250,
                                header_name='FFB Price/kg (Actual Production)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            grid_options2 = builder2.build()

                            # Display AgGrid
                            ag2 = AgGrid(st.session_state['ffbrefprice_FFBPriceList'],
                                        gridOptions=grid_options2,
                                        editable=False,
                                        allow_unsafe_jscode=True,
                                        theme='balham',
                                        height=500,
                                        fit_columns_on_grid_load=True,
                                        reload_data=False,
                                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                        custom_css={
                                            '#gridToolBar': {
                                                'padding-bottom': '0px !important'
                                            }
                                        })
                    else:
                        st.session_state['ffbrefprice_FFBPriceList'] = []
                        
                        ag2 = AgGrid(pd.DataFrame([]),
                                    editable=False,
                                    allow_unsafe_jscode=True,
                                    theme='balham',
                                    height=500,
                                    fit_columns_on_grid_load=True,
                                    reload_data=False,
                                    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                    custom_css={
                                        '#gridToolBar': {
                                            'padding-bottom': '0px !important'
                                        }
                                    })  
                
                # with st.container():
                #     with col18_2:
                #         # Average FFB Unit Price
                #         if len(ag['selected_rows']) == 1:
                #             st.session_state['yieldassess_AvgUnitPrice_Detail'] = float(ag['selected_rows'][0]['Average FFB Unit Price'])
                #         st.number_input('Average FFB Unit Price', key='yieldassess_AvgUnitPrice_Detail', disabled=True, format='%0.6f')  

                #         # Total Weight (kg)
                #         if len(ag['selected_rows']) == 1:
                #             st.session_state['yieldassess_TotalWeight_Detail'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                #         st.number_input('Total Weight (kg)', key='yieldassess_TotalWeight_Detail', disabled=True, format='%0.2f')
                        
                #         # Total Amount
                #         if len(ag['selected_rows']) == 1:
                #             st.session_state['yieldassess_TotalAmount_Detail'] = float(ag['selected_rows'][0]['Total FFB Procurement Amount'])
                #         st.number_input('Total Amount', key='yieldassess_TotalAmount_Detail', disabled=True)    
                    
                #         # OER (%)
                #         if len(ag['selected_rows']) == 1:
                #             st.session_state['yieldassess_OERBuying_Detail'] = float(ag['selected_rows'][0]['FFB Procurement OER'])
                #         st.number_input('OER (%)', key='yieldassess_OERBuying_Detail', disabled=True, format='%0.2f')  
            
            with st.container():
                with col17_2:
                    if len(st.session_state['ffbrefprice_RecordList']) != 0 and len(ag['selected_rows']) == 1 and len(st.session_state['ffbrefprice_FFBPriceList']) != 0:
                        st.download_button(
                            "Download as excel",
                            data=to_excel(pd.DataFrame(st.session_state['ffbrefprice_FFBPriceList']).set_index('OER (%)')),
                            file_name="FFB Reference Price by OER.xlsx",
                            mime="application/vnd.ms-excel",
                            use_container_width=True
                        )
                    else:
                        st.markdown('#')    
                    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['ffbrefprice_Status'] == 'Submit':
            statusMsg.info(st.session_state['ffbrefprice_Message'])
        elif st.session_state['ffbrefprice_Status'] == 'New':
            statusMsg.success(st.session_state['ffbrefprice_Message'])
        elif st.session_state['ffbrefprice_Status'] == 'Edit':
            statusMsg.error(st.session_state['ffbrefprice_Message'])
            
def hide_StatusMsg():
    statusMsgSection.empty()
    

    
with pageSection:
    st.subheader('FFB Reference Price')
    statusMsg = st.empty()
    
    show_MainPage()
    

        
        
