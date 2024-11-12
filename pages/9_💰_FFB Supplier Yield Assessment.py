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

url = st.secrets['url_SupYieldAssess']


#################################
# Session States Initialization #
#################################
if 'yieldassess_Status' not in st.session_state:
    st.session_state['yieldassess_Status'] = ''
    
if 'yieldassess_Message' not in st.session_state:
    st.session_state['yieldassess_Message'] = ''
    
if 'yieldassess_OUKey' not in st.session_state:
    st.session_state['yieldassess_OUKey'] = -1
    
    
# New, Edit, Delete, Cancel & Submit Button Disabled Status
if 'yieldassess_btnNew_disabled' not in st.session_state:
    st.session_state['yieldassess_btnNew_disabled'] = False

if 'yieldassess_btnEdit_disabled' not in st.session_state: 
    st.session_state['yieldassess_btnEdit_disabled'] = False
    
if 'yieldassess_btnDelete_disabled' not in st.session_state: 
    st.session_state['yieldassess_btnDelete_disabled'] = False
    
if 'yieldassess_btnCancel_disabled' not in st.session_state: 
    st.session_state['yieldassess_btnCancel_disabled'] = True
    
if 'yieldassess_btnSubmit_disabled' not in st.session_state: 
    st.session_state['yieldassess_btnSubmit_disabled'] = True
    

# From Date, To Date and Grid        
today = datetime.now()
    
if 'yieldassess_FromDate' not in st.session_state:
    st.session_state['yieldassess_FromDate'] = datetime(today.year, today.month, 1)
    
if 'yieldassess_ToDate' not in st.session_state:
    st.session_state['yieldassess_ToDate'] = today

if 'yieldassess_RecordList' not in st.session_state:
    st.session_state['yieldassess_RecordList'] = []


# Mill and Date
if 'yieldassess_Mill' not in st.session_state:
    st.session_state['yieldassess_Mill'] = st.session_state['yieldassess_OUKey']  #'LIBO SAWIT PERKASA PALM OIL MILL'
    
# if 'yieldassess_Mill_disabled' not in st.session_state:
#     st.session_state['yieldassess_Mill_disabled'] = True
    
if 'yieldassess_Date' not in st.session_state:
    st.session_state['yieldassess_Date'] = datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S")

if 'yieldassess_Date_disabled' not in st.session_state:
    st.session_state['yieldassess_Date_disabled'] = True
    
    
# CPO Price    
if 'yieldassess_CPOTdPrice' not in st.session_state:
    st.session_state['yieldassess_CPOTdPrice'] = 0.00
    
if 'yieldassess_CPOTdPrice_disabled' not in st.session_state:
    st.session_state['yieldassess_CPOTdPrice_disabled'] = True
    
if 'yieldassess_CPOProCharges' not in st.session_state:
    st.session_state['yieldassess_CPOProCharges'] = 0.00
    
if 'yieldassess_CPOProCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_CPOProCharges_disabled'] = True
    
if 'yieldassess_CPOTransCharges' not in st.session_state:
    st.session_state['yieldassess_CPOTransCharges'] = 0.00

if 'yieldassess_CPOTransCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_CPOTransCharges_disabled'] = True
    
if 'yieldassess_CPOPrice' not in st.session_state:
    st.session_state['yieldassess_CPOPrice'] = 0.00
    

# PK Price
if 'yieldassess_PKTdPrice' not in st.session_state:
    st.session_state['yieldassess_PKTdPrice'] = 0.00
    
if 'yieldassess_PKTdPrice_disabled' not in st.session_state:
    st.session_state['yieldassess_PKTdPrice_disabled'] = True

if 'yieldassess_PKProCharges' not in st.session_state:
    st.session_state['yieldassess_PKProCharges'] = 0.00

if 'yieldassess_PKProCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_PKProCharges_disabled'] = True
    
if 'yieldassess_PKTransCharges' not in st.session_state:
    st.session_state['yieldassess_PKTransCharges'] = 0.00

if 'yieldassess_PKTransCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_PKTransCharges_disabled'] = True

if 'yieldassess_RendPK' not in st.session_state:
    st.session_state['yieldassess_RendPK'] = 0.00

if 'yieldassess_RendPK_disabled' not in st.session_state:
    st.session_state['yieldassess_RendPK_disabled'] = True

if 'yieldassess_PKPrice' not in st.session_state:
    st.session_state['yieldassess_PKPrice'] = 0.00


# Shell Price  
if 'yieldassess_ShellTdPrice' not in st.session_state:
    st.session_state['yieldassess_ShellTdPrice'] = 0.00

if 'yieldassess_ShellTdPrice_disabled' not in st.session_state:
    st.session_state['yieldassess_ShellTdPrice_disabled'] = True

if 'yieldassess_ShellProCharges' not in st.session_state:
    st.session_state['yieldassess_ShellProCharges'] = 0.00

if 'yieldassess_ShellProCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_ShellProCharges_disabled'] = True
    
if 'yieldassess_ShellTransCharges' not in st.session_state:
    st.session_state['yieldassess_ShellTransCharges'] = 0.00

if 'yieldassess_ShellTransCharges_disabled' not in st.session_state:
    st.session_state['yieldassess_ShellTransCharges_disabled'] = True

if 'yieldassess_RendShell' not in st.session_state:
    st.session_state['yieldassess_RendShell'] = 0.00

if 'yieldassess_RendShell_disabled' not in st.session_state:
    st.session_state['yieldassess_RendShell_disabled'] = True

if 'yieldassess_ShellPrice' not in st.session_state:
    st.session_state['yieldassess_ShellPrice'] = 0.00

# Margin
if 'yieldassess_Margin' not in st.session_state:
    st.session_state['yieldassess_Margin'] = 0.00

# FFB Procurement OER, Total FFB Receipt (kg), Average FFB Unit Price, Total FFB Procurement Amount    
# FFB Procurement OER
if 'yieldassess_OERBuying' not in st.session_state:
    st.session_state['yieldassess_OERBuying'] = 0.00
    
# Total FFB Receipt (kg)
if 'yieldassess_TotalWeight' not in st.session_state:
    st.session_state['yieldassess_TotalWeight'] = 0.00

# Average FFB Unit Price
if 'yieldassess_AvgUnitPrice' not in st.session_state:
    st.session_state['yieldassess_AvgUnitPrice'] = 0.00
    
# Total FFB Procurement Amount
if 'yieldassess_TotalAmount' not in st.session_state:
    st.session_state['yieldassess_TotalAmount'] = 0.00
    
# Actual OER
if 'yieldassess_ProdOER' not in st.session_state:
    st.session_state['yieldassess_ProdOER'] = 0.00

# Total FFB Receit for (CPO Revenue)
if 'yieldassess_TotalWeight_CPORev' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_CPORev'] = 0.00
    
# CPO Tender Price for (CPO Revenue)
if 'yieldassess_CPOTdPrice_CPORev' not in st.session_state:
    st.session_state['yieldassess_CPOTdPrice_CPORev'] = 0.00
    
# CPO Revenue
if 'yieldassess_TotalCPOSellPrice' not in st.session_state:
    st.session_state['yieldassess_TotalCPOSellPrice'] = 0.00

# Actual KER
if 'yieldassess_ProdKER' not in st.session_state:
    st.session_state['yieldassess_ProdKER'] = 0.00

# Total FFB Receipt for (PK Revenue)
if 'yieldassess_TotalWeight_PKRev' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_PKRev'] = 0.00

# PK Tender Price for (PK Revenue)
if 'yieldassess_PKTdPrice_PKRev' not in st.session_state:
    st.session_state['yieldassess_PKTdPrice_PKRev'] = 0.00

# PK Revenue
if 'yieldassess_TotalPKSellPrice' not in st.session_state:
    st.session_state['yieldassess_TotalPKSellPrice'] = 0.00

# Actual SER
if 'yieldassess_ProdSER' not in st.session_state:
    st.session_state['yieldassess_ProdSER'] = 0.00
    
if 'yieldassess_ProdSER_disabled' not in st.session_state:
    st.session_state['yieldassess_ProdSER_disabled'] = True  
    
# Total FFB Weight for (Shell Revenue)
if 'yieldassess_TotalWeight_ShellRev' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_ShellRev'] = 0.00

# Shell Tender Price for (Shell Revenue)
if 'yieldassess_ShellTdPrice_ShellRev' not in st.session_state:
    st.session_state['yieldassess_ShellTdPrice_ShellRev'] = 0.00

# Shell Revenue
if 'yieldassess_TotalShSellPrice' not in st.session_state:
    st.session_state['yieldassess_TotalShSellPrice'] = 0.00

# Total Revenue
if 'yieldassess_TotalRevenue' not in st.session_state:
    st.session_state['yieldassess_TotalRevenue'] = 0.00

# Total RFB Receipt for (Expenses)
if 'yieldassess_TotalWeight_Exp' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_Exp'] = 0.00

# Average FFB Unit Price for (Expenses)
if 'yieldassess_AvgUnitPrice_Exp' not in st.session_state:
    st.session_state['yieldassess_AvgUnitPrice_Exp'] = 0.00

# Total FFB Procurement Amount for (Expenses)
if 'yieldassess_TotalAmount_Exp' not in st.session_state:
    st.session_state['yieldassess_TotalAmount_Exp'] = 0.00

# Total CPO Produced for (Expenses)
if 'yieldassess_TotalCPOProduced' not in st.session_state:
    st.session_state['yieldassess_TotalCPOProduced'] = 0.00

# CPO Production Cost
if 'yieldassess_CPOProdCost' not in st.session_state:
    st.session_state['yieldassess_CPOProdCost'] = 0.00

if 'yieldassess_CPOProdCost_disabled' not in st.session_state:
    st.session_state['yieldassess_CPOProdCost_disabled'] = True
    
# Total CPO Production Cost
if 'yieldassess_TotalCPOProdCost' not in st.session_state:
    st.session_state['yieldassess_TotalCPOProdCost'] = 0.00

 # Total PK Produced
if 'yieldassess_TotalPKProduced' not in st.session_state:
    st.session_state['yieldassess_TotalPKProduced'] = 0.00
 
# PK Production Cost
if 'yieldassess_PKProdCost' not in st.session_state:
    st.session_state['yieldassess_PKProdCost'] = 0.00

if 'yieldassess_PKProdCost_disabled' not in st.session_state:
    st.session_state['yieldassess_PKProdCost_disabled'] = True
  
# Total PK Production Cost
if 'yieldassess_TotalPKProdCost' not in st.session_state:
    st.session_state['yieldassess_TotalPKProdCost'] = 0.00
  
# Total FFB Receipt for (Kandir)
if 'yieldassess_TotalWeight_KandirExp' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_KandirExp'] = 0.00
  
# Kandir Cost
if 'yieldassess_KandirCost' not in st.session_state:
    st.session_state['yieldassess_KandirCost'] = 0.00

if 'yieldassess_KandirCost_disabled' not in st.session_state:
    st.session_state['yieldassess_KandirCost_disabled'] = True
    
# Total Kandir Cost
if 'yieldassess_TotalKandirCost' not in st.session_state:
    st.session_state['yieldassess_TotalKandirCost'] = 0.00

# Total CPO Produced for (Transport Cost)
if 'yieldassess_TotalCPOProduced_TransCost' not in st.session_state:
    st.session_state['yieldassess_TotalCPOProduced_TransCost'] = 0.00

# CPO Transport Cost
if 'yieldassess_CPOTransCost' not in st.session_state:
    st.session_state['yieldassess_CPOTransCost'] = 0.00

if 'yieldassess_CPOTransCost_disabled' not in st.session_state:
    st.session_state['yieldassess_CPOTransCost_disabled'] = True

# Total CPO Transport Cost
if 'yieldassess_TotalCPOTransCost' not in st.session_state:
    st.session_state['yieldassess_TotalCPOTransCost'] = 0.00

# Total PK Produced for (Transport Cost)
if 'yieldassess_TotalPKProduced_TransCost' not in st.session_state:
    st.session_state['yieldassess_TotalPKProduced_TransCost'] = 0.00

# PK Transport Cost
if 'yieldassess_PKTransCost' not in st.session_state:
    st.session_state['yieldassess_PKTransCost'] = 0.00

if 'yieldassess_PKTransCost_disabled' not in st.session_state:
    st.session_state['yieldassess_PKTransCost_disabled'] = True

# Total PK Transport Cost
if 'yieldassess_TotalPKTransCost' not in st.session_state:
    st.session_state['yieldassess_TotalPKTransCost'] = 0.00

# Total FFB Receipt for (Shrinkage Cost)
if 'yieldassess_TotalWeight_ShrinkageExp' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_ShrinkageExp'] = 0.00

# Shrinkage Cost
if 'yieldassess_ShrinkageCost' not in st.session_state:
    st.session_state['yieldassess_ShrinkageCost'] = 0.00

if 'yieldassess_ShrinkageCost_disabled' not in st.session_state:
    st.session_state['yieldassess_ShrinkageCost_disabled'] = True

# Total Shrinkage Cost
if 'yieldassess_TotalShrinkageCost' not in st.session_state:
    st.session_state['yieldassess_TotalShrinkageCost'] = 0.00
    
# Total Expenses
if 'yieldassess_TotalExpenses' not in st.session_state:
    st.session_state['yieldassess_TotalExpenses'] = 0.00



# Supplier Pricing & OER (Second Tab)
if 'yieldassess_SupplierList' not in st.session_state:
    st.session_state['yieldassess_SupplierList'] = []

# Average FFB Unit Price (Second Tab)
if 'yieldassess_AvgUnitPrice_Detail' not in st.session_state:
    st.session_state['yieldassess_AvgUnitPrice_Detail'] = 0.00

# Total Weight (Second Tab)
if 'yieldassess_TotalWeight_Detail' not in st.session_state:
    st.session_state['yieldassess_TotalWeight_Detail'] = 0.00

# Total Amount (Second Tab)
if 'yieldassess_TotalAmount_Detail' not in st.session_state:
    st.session_state['yieldassess_TotalAmount_Detail'] = 0.00

# OER (%) (Second Tab)
if 'yieldassess_OERBuying_Detail' not in st.session_state:
    st.session_state['yieldassess_OERBuying_Detail'] = 0.00





    
    
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
[data-testid="stToolbar"] {display: none;}
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
        st.session_state['yieldassess_OUKey'] = 6
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 1':
        st.session_state['yieldassess_OUKey'] = 8
    elif ou == 'SEMUNAI SAWIT PERKASA PALM OIL MILL 2':
        st.session_state['yieldassess_OUKey'] = 9


# -- Trigger Azure Logic App to submit Supplier Yield Assessment --
async def SubmitPricing(Date, ouKey, CPOTdPrice, CPOProCharges, CPOTransCharges, 
                        PKTdPrice, PKProCharges, PKTransCharges, RendPK,
                        ShellTdPrice, ShellProCharges, ShellTransCharges, RendShell,
                        ProdSER,
                        CPOProdCost, PKProdCost, KandirCost, CPOTransCost, PKTransCost, ShrinkageCost):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Submit Yield Assessment',
            "Date": str(Date),
            "OUKey": ouKey,
            "CPOTdPrice": CPOTdPrice,
            "CPOProCharges":CPOProCharges,
            "CPOTransCharges": CPOTransCharges,
            "PKTdPrice": PKTdPrice,
            "PKProCharges": PKProCharges,
            "PKTransCharges": PKTransCharges,
            "RendPK": RendPK,
            "ShellTdPrice": ShellTdPrice,
            "ShellProCharges": ShellProCharges,
            "ShellTransCharges": ShellTransCharges,
            "RendShell": RendShell,
            "ProdSER": ProdSER,
            "CPOProdCost": CPOProdCost,
            "PKProdCost": PKProdCost,
            "KandirCost": KandirCost,
            "CPOTransCost": CPOTransCost,
            "PKTransCost": PKTransCost,
            "ShrinkageCost": ShrinkageCost,
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            st.session_state['yieldassess_Status'] = ''
            Cancel()
            
            st.session_state['yieldassess_btnNew_disabled'] = False
            st.session_state['yieldassess_btnEdit_disabled'] = False
            st.session_state['yieldassess_btnDelete_disabled'] = False
            st.session_state['yieldassess_btnCancel_disabled'] = True
            st.session_state['yieldassess_btnSubmit_disabled'] = True
            

def Submit(Date, ouKey, CPOTdPrice, CPOProCharges, CPOTransCharges, 
           PKTdPrice, PKProCharges, PKTransCharges, RendPK,
           ShellTdPrice, ShellProCharges, ShellTransCharges, RendShell,
           ProdSER,
           CPOProdCost, PKProdCost, KandirCost, CPOTransCost, PKTransCost, ShrinkageCost):
    st.session_state['yieldassess_Status'] = 'Submit'
    st.session_state['yieldassess_Message'] = 'Submitting...'
    
    st.session_state['yieldassess_btnNew_disabled'] = True
    st.session_state['yieldassess_btnEdit_disabled'] = True
    st.session_state['yieldassess_btnDelete_disabled'] = True
    st.session_state['yieldassess_btnCancel_disabled'] = True
    st.session_state['yieldassess_btnSubmit_disabled'] = True
    
    # hide_MainPage()
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(SubmitPricing(Date, ouKey, CPOTdPrice, CPOProCharges, CPOTransCharges, 
                                          PKTdPrice, PKProCharges, PKTransCharges, RendPK,
                                          ShellTdPrice, ShellProCharges, ShellTransCharges, RendShell,
                                          ProdSER,
                                          CPOProdCost, PKProdCost, KandirCost, CPOTransCost, PKTransCost, ShrinkageCost)) 
    
    Call_DisplayGridRecords(st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_FromDate'], st.session_state['yieldassess_ToDate'])   
    
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
                st.session_state['yieldassess_RecordList'] = df.sort_values('Date')
            else:
                st.session_state['yieldassess_RecordList'] = []

async def DisplaySupplierGridRecords(OUKey, Date):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Load Supplier Record List',
            "OUKey": OUKey,
            "Date": str(Date)
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            
            if len(data['ResultSets']) != 0:
                df = pd.DataFrame(data['ResultSets']['Table1'])
                st.session_state['yieldassess_SupplierList'] = df.sort_values('Crop Supplier')
            else:
                st.session_state['yieldassess_SupplierList'] = []


def Call_DisplayGridRecords(ouKey, fromDate, toDate):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DisplayGridRecords(ouKey, fromDate, toDate)) 

   
def Call_DisplaySupplierGridRecords(ouKey, Date):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DisplaySupplierGridRecords(ouKey, Date)) 
    

def New():
    st.session_state['yieldassess_btnNew_disabled'] = True
    st.session_state['yieldassess_btnEdit_disabled'] = True
    st.session_state['yieldassess_btnDelete_disabled'] = True
    st.session_state['yieldassess_btnCancel_disabled'] = False
    st.session_state['yieldassess_btnSubmit_disabled'] = False
    
    st.session_state['yieldassess_Status'] = 'New'
    st.session_state['yieldassess_Message'] = 'Adding New Record'
    
    # st.session_state['yieldassess_Mill_disabled'] = True
    st.session_state['yieldassess_Date_disabled'] = False
    
    EmptyRecords()
    ControlAllowEdit()

    
def ControlAllowEdit():
    st.session_state['yieldassess_CPOTdPrice_disabled'] = False
    st.session_state['yieldassess_CPOProCharges_disabled'] = False
    st.session_state['yieldassess_CPOTransCharges_disabled'] = False
    
    st.session_state['yieldassess_PKTdPrice_disabled'] = False
    st.session_state['yieldassess_PKProCharges_disabled'] = False
    st.session_state['yieldassess_PKTransCharges_disabled'] = False
    st.session_state['yieldassess_RendPK_disabled'] = False
    
    st.session_state['yieldassess_ShellTdPrice_disabled'] = False
    st.session_state['yieldassess_ShellProCharges_disabled'] = False
    st.session_state['yieldassess_ShellTransCharges_disabled'] = False
    st.session_state['yieldassess_RendShell_disabled'] = False 
    
    st.session_state['yieldassess_ProdSER_disabled'] = False
    
    st.session_state['yieldassess_CPOProdCost_disabled'] = False
    st.session_state['yieldassess_PKProdCost_disabled'] = False
    st.session_state['yieldassess_KandirCost_disabled'] = False
    st.session_state['yieldassess_CPOTransCost_disabled'] = False
    st.session_state['yieldassess_PKTransCost_disabled'] = False
    st.session_state['yieldassess_ShrinkageCost_disabled'] = False

    
def ControlNotAllowEdit():
    st.session_state['yieldassess_CPOTdPrice_disabled'] = True
    st.session_state['yieldassess_CPOProCharges_disabled'] = True
    st.session_state['yieldassess_CPOTransCharges_disabled'] = True
    
    st.session_state['yieldassess_PKTdPrice_disabled'] = True
    st.session_state['yieldassess_PKProCharges_disabled'] = True
    st.session_state['yieldassess_PKTransCharges_disabled'] = True
    st.session_state['yieldassess_RendPK_disabled'] = True
    
    st.session_state['yieldassess_ShellTdPrice_disabled'] = True
    st.session_state['yieldassess_ShellProCharges_disabled'] = True
    st.session_state['yieldassess_ShellTransCharges_disabled'] = True
    st.session_state['yieldassess_RendShell_disabled'] = True
    
    st.session_state['yieldassess_ProdSER_disabled'] = True
    
    st.session_state['yieldassess_CPOProdCost_disabled'] = True
    st.session_state['yieldassess_PKProdCost_disabled'] = True
    st.session_state['yieldassess_KandirCost_disabled'] = True
    st.session_state['yieldassess_CPOTransCost_disabled'] = True
    st.session_state['yieldassess_PKTransCost_disabled'] = True
    st.session_state['yieldassess_ShrinkageCost_disabled'] = True


def EmptyRecords():
    
    st.session_state['yieldassess_Date'] = datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S")
    
    # CPO Price
    st.session_state['yieldassess_CPOTdPrice'] = 0.00
    st.session_state['yieldassess_CPOProCharges'] = 0.00
    st.session_state['yieldassess_CPOTransCharges'] = 0.00
    
    # PK Price
    st.session_state['yieldassess_PKTdPrice'] = 0.00
    st.session_state['yieldassess_PKProCharges'] = 0.00
    st.session_state['yieldassess_PKTransCharges'] = 0.00
    st.session_state['yieldassess_RendPK'] = 0.00
    
    # Shell Price
    st.session_state['yieldassess_ShellTdPrice'] = 0.00
    st.session_state['yieldassess_ShellProCharges'] = 0.00
    st.session_state['yieldassess_ShellTransCharges'] = 0.00
    st.session_state['yieldassess_RendShell'] = 0.00
    
    # Margin
    st.session_state['yieldassess_Margin'] = 0.00
    
    # FFB Procurement OER
    st.session_state['yieldassess_OERBuying'] = 0.00
    
    # Total FFB Receipt (kg)
    st.session_state['yieldassess_TotalWeight'] = 0.00
    
    # Average FFB Unit Price
    st.session_state['yieldassess_AvgUnitPrice'] = 0.00
    
    # Total FFB Procurement Amount
    st.session_state['yieldassess_TotalAmount'] = 0.00
    
    # Actual OER (%)
    st.session_state['yieldassess_ProdOER'] = 0.00
    
    # Total FFB Weight for (CPO Revenue)
    st.session_state['yieldassess_TotalWeight_CPORev'] = 0.00
    
    # CPO Tender Price
    st.session_state['yieldassess_CPOTdPrice_CPORev'] = 0.00
    
    # CPO Revenue
    st.session_state['yieldassess_TotalCPOSellPrice'] = 0.00
    
    # Actual KER (%)
    st.session_state['yieldassess_ProdKER'] = 0.00
    
    # Total FFB Weight for (PK Revenue)
    st.session_state['yieldassess_TotalWeight_PKRev'] = 0.00
    
    # PK Tender Price
    st.session_state['yieldassess_PKTdPrice_PKRev'] = 0.00
    
    # PK Revenue
    st.session_state['yieldassess_TotalPKSellPrice'] = 0.00
    
    # Actual SER (%)
    st.session_state['yieldassess_ProdSER'] = 0.00
    
    # Total FFB Receipt for (Shell Revenue)
    st.session_state['yieldassess_TotalWeight_ShellRev'] = 0.00
    
    # Shell Tender Price for (Shell Revenue)
    st.session_state['yieldassess_ShellTdPrice_ShellRev'] = 0.00
    
    # Shell Revenue
    st.session_state['yieldassess_TotalShSellPrice'] = 0.00
    
    # Total Revenue
    st.session_state['yieldassess_TotalRevenue'] = 0.00
    
    # Total FFB Receipt (kg)
    st.session_state['yieldassess_TotalWeight_Exp'] = 0.00
    
    # Average FFB Unit Price
    st.session_state['yieldassess_AvgUnitPrice_Exp'] = 0.00
    
    # Total FFB Procurement Amount
    st.session_state['yieldassess_TotalAmount_Exp'] = 0.00
    
    # Total CPO Produced (kg)
    st.session_state['yieldassess_TotalCPOProduced'] = 0.00
    
    # CPO Production Cost
    st.session_state['yieldassess_CPOProdCost'] = 0.00
    
    # Total CPO Production Cost
    st.session_state['yieldassess_TotalCPOProdCost'] = 0.00
    
    # Total PK Produced (kg)
    st.session_state['yieldassess_TotalPKProduced'] = 0.00
    
    # PK Production Cost
    st.session_state['yieldassess_PKProdCost'] = 0.00
    
    # Total PK Production Cost
    st.session_state['yieldassess_TotalPKProdCost'] = 0.00
    
    # Total FFB Receipt (kg)
    st.session_state['yieldassess_TotalWeight_KandirExp'] = 0.00
    
    # Kandir Cost
    st.session_state['yieldassess_KandirCost'] = 0.00
    
    # Total Kandir Cost
    st.session_state['yieldassess_TotalKandirCost'] = 0.00
    
    # Total CPO Produced (kg)
    st.session_state['yieldassess_TotalCPOProduced_TransCost'] = 0.00
    
    # CPO Transport Cost
    st.session_state['yieldassess_CPOTransCost'] = 0.00
    
    # Total CPO Transport Cost
    st.session_state['yieldassess_TotalCPOTransCost'] = 0.00
    
    # Total PK Produced (kg)
    st.session_state['yieldassess_TotalPKProduced_TransCost'] = 0.00
    
    # PK Transport Cost
    st.session_state['yieldassess_PKTransCost'] = 0.00
    
    # Total PK Transport Cost
    st.session_state['yieldassess_TotalPKTransCost'] = 0.00
    
    # Total FFB Receipt (kg)
    st.session_state['yieldassess_TotalWeight_ShrinkageExp'] = 0.00
    
    # Skrinkage Cost
    st.session_state['yieldassess_ShrinkageCost'] = 0.00
    
    # Total Shrinkage Cost
    st.session_state['yieldassess_TotalShrinkageCost'] = 0.00
    
    # Total Expenses
    st.session_state['yieldassess_TotalExpenses'] = 0.00
    
    # Profit & Loss
    st.session_state['yieldassess_ProfitAndLoss'] = 0.00
        
    
 
def Edit():
    st.session_state['yieldassess_Status'] = 'Edit'
    st.session_state['yieldassess_btnNew_disabled'] = True
    st.session_state['yieldassess_btnEdit_disabled'] = True
    st.session_state['yieldassess_btnDelete_disabled'] = True
    st.session_state['yieldassess_btnCancel_disabled'] = False
    st.session_state['yieldassess_btnSubmit_disabled'] = False
    
    # st.session_state['yieldassess_Mill_disabled'] = True
    st.session_state['yieldassess_Date_disabled'] = False
    
    ControlAllowEdit()
    
    
# -- Trigger Azure Logic App to delete Supplier Yield Assessment --
async def DeletePricing(Date, ouKey):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "Method": 'Delete Yield Assessment',
            "Date": str(Date),
            "OUKey": ouKey,
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
             
            

def Delete(Date, ouKey):
    st.session_state['YieldAssess_Status'] = 'Delete Record'
    st.session_state['YieldAssess_Message'] = 'Deleting Record...'
    
    st.session_state['yieldassess_btnNew_disabled'] = True
    st.session_state['yieldassess_btnEdit_disabled'] = True
    st.session_state['yieldassess_btnDelete_disabled'] = True
    st.session_state['yieldassess_btnCancel_disabled'] = True
    st.session_state['yieldassess_btnSubmit_disabled'] = True
    
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(DeletePricing(Date, ouKey)) 
    
    Call_DisplayGridRecords(st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_FromDate'], st.session_state['yieldassess_ToDate'])   
    EmptyRecords()
    Cancel()
            
    st.session_state['yieldassess_btnNew_disabled'] = False
    st.session_state['yieldassess_btnEdit_disabled'] = False
    st.session_state['yieldassess_btnDelete_disabled'] = False
    st.session_state['yieldassess_btnCancel_disabled'] = True
    st.session_state['yieldassess_btnSubmit_disabled'] = True
    
    st.markdown('#')
 
   
def Cancel():
    st.session_state['yieldassess_Status'] = ''
    st.session_state['yieldassess_btnNew_disabled'] = False
    st.session_state['yieldassess_btnEdit_disabled'] = False
    st.session_state['yieldassess_btnDelete_disabled'] = False
    st.session_state['yieldassess_btnCancel_disabled'] = True
    st.session_state['yieldassess_btnSubmit_disabled'] = True
    
    # st.session_state['yieldassess_Mill_disabled'] = True
    st.session_state['yieldassess_Date_disabled'] = True
    
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
        col22_1, col22_2 = st.columns([85, 15]) # Scroll links, Export to Excel
        col2_1, col2_2, col2_3 = st.columns([1, 98, 1]) # Grid
        
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
                st.session_state['yieldassess_FromDate'] = st.date_input('From Date', value=st.session_state['yieldassess_FromDate'], format="DD/MM/YYYY")
            
            with col1_3:
                st.session_state['yieldassess_ToDate'] = st.date_input('To Date', value=st.session_state['yieldassess_ToDate'], format="DD/MM/YYYY")
                
            with col1_4:
                st.markdown('####')
                st.button('Refresh',
                        on_click=Call_DisplayGridRecords,
                        args=(st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_FromDate'], st.session_state['yieldassess_ToDate']),
                        help='Click to refresh grid records.',
                        use_container_width=True)

        # Scroll links, Export to Excel
        with st.container():
            with col22_1:
                st.markdown('[Scroll to Pricing](#pricing) | [Scroll to Expenses](#expenses)')
            with col22_2:
                if len(st.session_state['yieldassess_RecordList']) != 0:
                    st.download_button(
                        "Download as excel",
                        data=to_excel(pd.DataFrame(st.session_state['yieldassess_RecordList']).set_index('Date')),
                        file_name="FFB Supplier Yield Assessment.xlsx",
                        mime="application/vnd.ms-excel",
                        use_container_width=True
                    )
                else:
                    st.markdown('#')

        #####################
        # Grid with Records #
        #####################
        with st.container():
            with col2_2:
            # if len(st.session_state['yieldassess_RecordList']) == 0:
            #     Call_DisplayGridRecords(st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_FromDate'], st.session_state['yieldassess_ToDate'])
            
                # Configure grid options using GridOptionsBuilder
                if len(st.session_state['yieldassess_RecordList']) != 0:
                    builder = GridOptionsBuilder.from_dataframe(st.session_state['yieldassess_RecordList'])
                
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
                        field='FFB Procurement OER',
                        header_name='FFB Procurement OER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Total FFB Receipt',
                        header_name='Total FFB Receipt (kg)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual OER',
                        header_name='Actual OER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual KER',
                        header_name='Actual KER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    builder.configure_column(
                        field='Actual SER',
                        header_name='Actual SER (%)',
                        type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                        precision=2
                    )
                    grid_options = builder.build()

                    # Display AgGrid
                    ag = AgGrid(st.session_state['yieldassess_RecordList'],
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
        tab1, tab2 = st.tabs(['Calculation', 'Supplier Pricing & OER'])
        
        with tab1:
            col3_1, col3_2, col3_3, col3_4, col3_5, col3_6, col3_7= st.columns([25, 25, 10, 10, 10, 10, 10]) # Mill and Date
            
            # Create an anchor point at here
            st.markdown('<a name="pricing"></a>', unsafe_allow_html=True)
            
            st.info('##### Pricing')
            st.markdown('[Scroll to Expenses](#expenses) | [Scroll to Top](#top)')
            st.markdown('###### CPO Pricing')
            col4_1, col4_2, col4_3, col4_4, col4_5, col4_6, col4_7, col4_8, col4_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # CPO Pricing
            
            st.markdown('###### PK Pricing')
            col5_1, col5_2, col5_3, col5_4, col5_5, col5_6, col5_7, col5_8, col5_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # PK Pricing
            
            st.markdown('###### Shell Pricing')
            col6_1, col6_2, col6_3, col6_4, col6_5, col6_6, col6_7, col6_8, col6_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # Shell Pricing
            
            col7_1, col7_2 = st.columns([20, 80]) # Margin
            
            col8_1, col8_2, col8_3, col8_4, col8_5, col8_6, col8_7, col8_8, col8_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # FFB Procurement OER, Total FFB Receipt (kg), Average FFB Unit Price, Total FFB Procurement Amount
            
            st.success('##### Revenue')
            col9_1, col9_2, col9_3, col9_4, col9_5, col9_6, col9_7, col9_8, col9_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # CPO Revenue
            col10_1, col10_2, col10_3, col10_4, col10_5, col10_6, col10_7, col10_8, col10_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # PK Revenue
            col11_1, col11_2, col11_3, col11_4, col11_5, col11_6, col11_7, col11_8, col11_9 = st.columns([20, 2, 18, 2, 18, 2, 18, 2, 18]) # Shell Revenue
            col12_1, col12_2 = st.columns([82, 18]) # Total Revenue
            
            # Create an anchor point at here
            st.markdown('<a name="expenses"></a>', unsafe_allow_html=True)
            
            st.error('##### Expenses')
            
            col13_1, col13_2, col13_3, col13_4, col13_5, col13_6 = st.columns([42, 18, 2, 18, 2, 18]) # FFB Procurement Amount
            col14_1, col14_2, col14_3, col14_4, col14_5, col14_6 = st.columns([42, 18, 2, 18, 2, 18]) # CPO Production Cost
            col15_1, col15_2, col15_3, col15_4, col15_5, col15_6 = st.columns([42, 18, 2, 18, 2, 18]) # PK Production Cost
            col16_1, col16_2, col16_3, col16_4, col16_5, col16_6 = st.columns([42, 18, 2, 18, 2, 18]) # Kandir Cost
            col17_1, col17_2, col17_3, col17_4, col17_5, col17_6 = st.columns([42, 18, 2, 18, 2, 18]) # CPO Transport Cost
            col18_1, col18_2, col18_3, col18_4, col18_5, col18_6 = st.columns([42, 18, 2, 18, 2, 18]) # PK Transport Cost
            col19_1, col19_2, col19_3, col19_4, col19_5, col19_6 = st.columns([42, 18, 2, 18, 2, 18]) # Shrinkage Cost
            col20_1, col20_2 = st.columns([82, 18]) # Total Expenses
            
            col21_1, col21_2 = st.columns([82, 18]) # Profit & Loss`
            
        
        
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
            
            # st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"ColorMeBlue text”"}</h1>', unsafe_allow_html=True)
            # st.markdown("""
            #             <style>
            #             .stTextArea [data-baseweb=base-input] {
            #                 background-image: linear-gradient(140deg, rgb(54, 36, 31) 0%, rgb(121, 56, 100) 50%, rgb(106, 117, 25) 75%);
            #                 -webkit-text-fill-color: white;
            #             }

            #             .stTextArea [data-baseweb=base-input] [disabled=""]{
            #                 background-image: linear-gradient(45deg, red, purple, red);
            #                 -webkit-text-fill-color: gray;
            #             }
            #             </style>
            #             """,unsafe_allow_html=True)

            # disable_textarea = st.checkbox("Disable text area:")

            # st.text_area(
            #     label="Text area:",
            #     value="This is a repeated sentence "*20,
            #     height=300,
            #     disabled=disable_textarea)
            
            
            # if st.button("Scroll to Top"):
            #     # Use JavaScript to scroll to the top of the page
            #     st.write(
            #         """
            #         <script>
            #         window.scrollTo({ top: 0, behavior: 'smooth' });
            #         </script>
            #         """
            #     )
            
            
            
            ######################################################
            # Mill, Date, New Record, Edit Record, Submit Record #
            ######################################################
            with st.container():
                with col3_1:
                    # if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                    st.session_state['yieldassess_Mill'] = ou
                    
                    st.selectbox('Mill', options=('LIBO SAWIT PERKASA PALM OIL MILL',
                                                'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
                                                'SEMUNAI SAWIT PERKASA PALM OIL MILL 2'),  
                                key='yieldassess_Mill', disabled=True)

                    get_OUKey(st.session_state['yieldassess_Mill'])
                    
                with col3_2:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_Date'] = datetime.strptime(ag['selected_rows'][0]['Date'], "%Y-%m-%dT%H:%M:%S") if len(ag['selected_rows']) == 1 else datetime.strptime((datetime.today() - timedelta(days=1)).replace(microsecond=0).isoformat(), "%Y-%m-%dT%H:%M:%S") # datetime.strptime('1900-01-01T00:00:00', "%Y-%m-%dT%H:%M:%S")
                    st.date_input('Date', key='yieldassess_Date', disabled=st.session_state['yieldassess_Date_disabled'], format="DD/MM/YYYY")
                    
                with col3_3:
                    st.markdown('#')
                    st.button('New Record',
                            on_click=New,
                            args=(),
                            help='Click to add new record.',
                            disabled=st.session_state['yieldassess_btnNew_disabled'],
                            use_container_width=True)
                with col3_4:
                    st.markdown('#')
                    st.button('Edit Record',
                            on_click=Edit,
                            args=(),
                            help='Click to edit record.',
                            disabled=st.session_state['yieldassess_btnEdit_disabled'],
                            use_container_width=True)
                with col3_5:
                    st.markdown('#')
                    st.button('Delete',
                            on_click=Delete,
                            args=(st.session_state['yieldassess_Date'], st.session_state['yieldassess_OUKey']),
                            help='Click to delete this record.',
                            disabled=st.session_state['yieldassess_btnDelete_disabled'],
                            use_container_width=True)
                with col3_6:
                    st.markdown('#')
                    st.button('Cancel',
                            on_click=Cancel,
                            args=(),
                            help='Click to cancel add or edit record.',
                            disabled=st.session_state['yieldassess_btnCancel_disabled'],
                            use_container_width=True)
                with col3_7:
                    st.markdown('#')
                    st.button('Submit',
                            on_click=Submit,
                            args=(st.session_state['yieldassess_Date'], st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_CPOTdPrice'], st.session_state['yieldassess_CPOProCharges'], 
                                st.session_state['yieldassess_CPOTransCharges'], st.session_state['yieldassess_PKTdPrice'], st.session_state['yieldassess_PKProCharges'], 
                                st.session_state['yieldassess_PKTransCharges'], st.session_state['yieldassess_RendPK'],
                                st.session_state['yieldassess_ShellTdPrice'], st.session_state['yieldassess_ShellProCharges'], 
                                st.session_state['yieldassess_ShellTransCharges'], st.session_state['yieldassess_RendShell'],
                                st.session_state['yieldassess_ProdSER'],
                                st.session_state['yieldassess_CPOProdCost'], st.session_state['yieldassess_PKProdCost'],
                                st.session_state['yieldassess_KandirCost'], st.session_state['yieldassess_CPOTransCost'],
                                st.session_state['yieldassess_PKTransCost'], st.session_state['yieldassess_ShrinkageCost']),
                            help='Click to submit record.',
                            disabled=st.session_state['yieldassess_btnSubmit_disabled'],
                            use_container_width=True)
            
                
            
            #############################
            # CPO, PK and Shell Pricing #
            #############################
            # CPO Pricing
            with st.container():
                with col4_1:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_CPOTdPrice'] = float(ag['selected_rows'][0]['CPO Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_CPOTdPrice']
                    st.number_input('CPO Tender Price', key='yieldassess_CPOTdPrice', disabled=st.session_state['yieldassess_CPOTdPrice_disabled'])
                with col4_2:
                    st.markdown('###')
                    st.markdown('### -')
                with col4_3:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_CPOProCharges'] = float(ag['selected_rows'][0]['CPO Produced Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_CPOProCharges']
                    st.number_input('CPO Production Charges', key='yieldassess_CPOProCharges', disabled=st.session_state['yieldassess_CPOProCharges_disabled'])
                with col4_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col4_5:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_CPOTransCharges'] = float(ag['selected_rows'][0]['CPO Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_CPOTransCharges']
                    st.number_input('CPO Transport Charges', key='yieldassess_CPOTransCharges', disabled=st.session_state['yieldassess_CPOTransCharges_disabled'])
                with col4_6:
                    st.markdown('#')
                with col4_7:
                    st.markdown('#')
                with col4_8:
                    st.markdown('###')
                    st.markdown('### =')
                with col4_9:
                    st.session_state['yieldassess_CPOPrice'] = format(float(st.session_state['yieldassess_CPOTdPrice'] - st.session_state['yieldassess_CPOProCharges'] - st.session_state['yieldassess_CPOTransCharges']), '.0f')
                    st.text_input('CPO Price', key='yieldassess_CPOPrice', disabled=True)
        
            # PK Pricing
            with st.container():
                with col5_1:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_PKTdPrice'] = float(ag['selected_rows'][0]['PK Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_PKTdPrice']
                    st.number_input('PK Tender Price', key='yieldassess_PKTdPrice', disabled=st.session_state['yieldassess_PKTdPrice_disabled'])
                with col5_2:
                    st.markdown('###')
                    st.markdown('### -')
                with col5_3:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_PKProCharges'] = float(ag['selected_rows'][0]['PK Produced Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_PKProCharges']
                    st.number_input('PK Production Charges', key='yieldassess_PKProCharges', disabled=st.session_state['yieldassess_PKProCharges_disabled'])
                with col5_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col5_5:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_PKTransCharges'] = float(ag['selected_rows'][0]['PK Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_PKTransCharges']
                    st.number_input('PK Transport Charges', key='yieldassess_PKTransCharges', disabled=st.session_state['yieldassess_PKTransCharges_disabled'])
                with col5_6:
                    st.markdown('###')
                    st.markdown('### x')
                with col5_7:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_RendPK'] = float(ag['selected_rows'][0]['Rend PK']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_RendPK']
                    st.number_input('Rend PK (%)', key='yieldassess_RendPK', disabled=st.session_state['yieldassess_RendPK_disabled'])
                with col5_8:
                    st.markdown('###')
                    st.markdown('### =')
                with col5_9:
                    st.session_state['yieldassess_PKPrice'] = format(float((st.session_state['yieldassess_PKTdPrice'] - st.session_state['yieldassess_PKProCharges'] - st.session_state['yieldassess_PKTransCharges']) * st.session_state['yieldassess_RendPK'] / 100), '.0f')
                    st.text_input('PK Price', key='yieldassess_PKPrice', disabled=True)

            # Shell Pricing
            with st.container():
                with col6_1:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_ShellTdPrice'] = float(ag['selected_rows'][0]['Shell Tender Price']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_ShellTdPrice']
                    st.number_input('Shell Tender Price', key='yieldassess_ShellTdPrice', disabled=st.session_state['yieldassess_ShellTdPrice_disabled'])
                with col6_2:
                    st.markdown('###')
                    st.markdown('### -')
                with col6_3:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_ShellProCharges'] = float(ag['selected_rows'][0]['Shell Produced Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_ShellProCharges']
                    st.number_input('Shell Production Charges', key='yieldassess_ShellProCharges', disabled=st.session_state['yieldassess_ShellProCharges_disabled'])
                with col6_4:
                    st.markdown('###')
                    st.markdown('### -')
                with col6_5:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_ShellTransCharges'] = float(ag['selected_rows'][0]['Shell Transport Charges']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_ShellTransCharges']
                    st.number_input('Shell Transport Charges', key='yieldassess_ShellTransCharges', disabled=st.session_state['yieldassess_ShellTransCharges_disabled'])
                with col6_6:
                    st.markdown('###')
                    st.markdown('### x')
                with col6_7:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_RendShell'] = float(ag['selected_rows'][0]['Rend Shell']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_RendShell']
                    st.number_input('Rend Shell (%)', key='yieldassess_RendShell', disabled=st.session_state['yieldassess_RendShell_disabled'])
                with col6_8:
                    st.markdown('###')
                    st.markdown('### =')
                with col6_9:
                    st.session_state['yieldassess_ShellPrice'] = format(float((st.session_state['yieldassess_ShellTdPrice'] - st.session_state['yieldassess_ShellProCharges'] - st.session_state['yieldassess_ShellTransCharges']) * st.session_state['yieldassess_RendShell'] / 100), '.0f')
                    st.text_input('Shell Price', key='yieldassess_ShellPrice', disabled=True)
                        
            # Margin 
            with st.container():
                with col7_1:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_Margin'] = float(ag['selected_rows'][0]['Margin'])
                    st.number_input('Margin', key='yieldassess_Margin', disabled=True)
                
                    
            #####################################################################################################
            # FFB Procurement OER, Total FFB Receipt (kg), Average FFB Unit Price, Total FFB Procurement Amount #
            #####################################################################################################
            with st.container():
                # FFB Procurement OER
                with col8_1:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_OERBuying'] = float(ag['selected_rows'][0]['FFB Procurement OER'])
                    st.number_input('FFB Procurement OER', key='yieldassess_OERBuying', disabled=True, format='%0.2f')  
            
                with col8_2:
                    st.markdown("#")
                
                # Total FFB Receipt (kg)
                with col8_3:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight', disabled=True, format='%0.2f')  
                
                with col8_4:
                    st.markdown("#")
                
                # Average FFB Unit Price
                with col8_5:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_AvgUnitPrice'] = float(ag['selected_rows'][0]['Average FFB Unit Price'])
                    st.number_input('Average FFB Unit Price', key='yieldassess_AvgUnitPrice', disabled=True, format='%0.6f')  
                
                with col8_6:
                    st.markdown("#")
                
                with col8_7:
                    st.markdown("#")
                    
                with col8_8:
                    st.markdown("#")
                
                # Total FFB Procurement Amount
                with col8_9:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalAmount'] = float(ag['selected_rows'][0]['Total FFB Procurement Amount'])
                    st.number_input('Total FFB Procurement Amount', key='yieldassess_TotalAmount', disabled=True)       
            
            
            ###########
            # Revenue #
            ###########
            # CPO Revenue
            with st.container():
                with col9_1:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_ProdOER'] = float(ag['selected_rows'][0]['Actual OER'])
                    st.number_input('Actual OER (%)', key='yieldassess_ProdOER', disabled=True)
                with col9_2:
                    st.markdown('###')
                    st.markdown('### x')
                with col9_3:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_CPORev'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_CPORev', disabled=True, format='%0.2f')  
                with col9_4:
                    st.markdown('###')
                    st.markdown('### x')
                with col9_5:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_CPOTdPrice_CPORev'] = float(ag['selected_rows'][0]['CPO Tender Price'])
                    st.number_input('CPO Tender Price', key='yieldassess_CPOTdPrice_CPORev', disabled=True, format='%0.2f') 
                with col9_6:
                    st.markdown('#')
                with col9_7:
                    st.markdown('#')
                with col9_8:   
                    st.markdown('###')
                    st.markdown('### =')
                with col9_9:   
                    st.session_state['yieldassess_TotalCPOSellPrice'] = format(float((st.session_state['yieldassess_ProdOER'] / 100) * st.session_state['yieldassess_TotalWeight_CPORev'] * st.session_state['yieldassess_CPOTdPrice_CPORev']), '.2f')
                    st.text_input('CPO Revenue', key='yieldassess_TotalCPOSellPrice', disabled=True)
                
            # PK Revenue
            with st.container():
                with col10_1:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_ProdKER'] = float(ag['selected_rows'][0]['Actual KER'])
                    st.number_input('Actual KER (%)', key='yieldassess_ProdKER', disabled=True)
                with col10_2:
                    st.markdown('###')
                    st.markdown('### x')
                with col10_3:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_PKRev'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_PKRev', disabled=True, format='%0.2f')  
                with col10_4:
                    st.markdown('###')
                    st.markdown('### x')
                with col10_5:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_PKTdPrice_PKRev'] = float(ag['selected_rows'][0]['PK Tender Price'])
                    st.number_input('PK Tender Price', key='yieldassess_PKTdPrice_PKRev', disabled=True, format='%0.2f') 
                with col10_6:
                    st.markdown('#')
                with col10_7:
                    st.markdown('#')
                with col10_8:   
                    st.markdown('###')
                    st.markdown('### =')
                with col10_9:   
                    st.session_state['yieldassess_TotalPKSellPrice'] = format(float((st.session_state['yieldassess_ProdKER'] / 100) * st.session_state['yieldassess_TotalWeight_PKRev'] * st.session_state['yieldassess_PKTdPrice_PKRev']), '.2f')
                    st.text_input('PK Revenue', key='yieldassess_TotalPKSellPrice', disabled=True) 
                    
            # Shell Revenue
            with st.container():
                with col11_1:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_ProdSER'] = float(ag['selected_rows'][0]['Actual SER'])
                    st.number_input('Actual SER (%)', key='yieldassess_ProdSER', disabled=st.session_state['yieldassess_ProdSER_disabled'])
                with col11_2:
                    st.markdown('###')
                    st.markdown('### x')
                with col11_3:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_ShellRev'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_ShellRev', disabled=True, format='%0.2f')  
                with col11_4:
                    st.markdown('###')
                    st.markdown('### x')
                with col11_5:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_ShellTdPrice_ShellRev'] = float(ag['selected_rows'][0]['Shell Tender Price'])
                    st.number_input('Shell Tender Price', key='yieldassess_ShellTdPrice_ShellRev', disabled=True, format='%0.2f') 
                with col11_6:
                    st.markdown('#')
                with col11_7:
                    st.markdown('#')
                with col11_8:   
                    st.markdown('###')
                    st.markdown('### =')
                with col11_9:   
                    st.session_state['yieldassess_TotalShSellPrice'] = format(float((st.session_state['yieldassess_ProdSER'] / 100) * st.session_state['yieldassess_TotalWeight_ShellRev'] * st.session_state['yieldassess_ShellTdPrice_ShellRev']), '.2f')
                    st.text_input('Shell Revenue', key='yieldassess_TotalShSellPrice', disabled=True) 
            
            # Total Revenue
            with st.container():
                with col12_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>Total Revenue : </h4>", unsafe_allow_html=True)
                with col12_2:
                    st.session_state['yieldassess_TotalRevenue'] = format(float(st.session_state['yieldassess_TotalCPOSellPrice']) + float(st.session_state['yieldassess_TotalPKSellPrice']) + float(st.session_state['yieldassess_TotalShSellPrice']), '.2f')
                    st.text_input('', key='yieldassess_TotalRevenue', disabled=True)
            
            ############
            # Expenses #
            ############   
            # FFB Procurement Amount
            with st.container():
                with col13_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>FFB Procurement Amount : </h4>", unsafe_allow_html=True)

                # Total FFB Receipt
                with col13_2:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_Exp'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_Exp', disabled=True, format='%0.2f')  

                with col13_3:
                    st.markdown('###')
                    st.markdown('### x')
            
                # Average FFB Unit Price
                with col13_4:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_AvgUnitPrice_Exp'] = float(ag['selected_rows'][0]['Average FFB Unit Price'])
                    st.number_input('Average FFB Unit Price', key='yieldassess_AvgUnitPrice_Exp', disabled=True, format='%0.2f')  
                
                with col13_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total FFB Procurement Amount
                with col13_6:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalAmount_Exp'] = float(ag['selected_rows'][0]['Total FFB Procurement Amount'])
                    st.number_input('Total FFB Procurement Amount', key='yieldassess_TotalAmount_Exp', disabled=True)  
                        
            # CPO Production Cost
            with st.container():
                with col14_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>CPO Production Cost : </h4>", unsafe_allow_html=True)
                    
                # Total CPO Produced (kg)
                with col14_2:
                    st.session_state['yieldassess_TotalCPOProduced'] = float((st.session_state['yieldassess_ProdOER'] / 100) * st.session_state['yieldassess_TotalWeight_CPORev'])
                    st.number_input('Total CPO Produced (kg)', key='yieldassess_TotalCPOProduced', disabled=True)

                with col14_3:
                    st.markdown('###')
                    st.markdown('### x')
                    
                # CPO Production Cost
                with col14_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_CPOProdCost'] = float(ag['selected_rows'][0]['CPO Production Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_CPOProdCost']
                    st.number_input('CPO Production Cost', key='yieldassess_CPOProdCost', disabled=st.session_state['yieldassess_CPOProdCost_disabled'])
            
                with col14_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total CPO Production Cost
                with col14_6: 
                    st.session_state['yieldassess_TotalCPOProdCost'] = format(float(st.session_state['yieldassess_TotalCPOProduced']) * float(st.session_state['yieldassess_CPOProdCost']), '.2f')
                    st.text_input('Total CPO Production Cost', key='yieldassess_TotalCPOProdCost', disabled=True)
                    
            # PK Production Cost
            with st.container():
                with col15_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>PK Production Cost : </h4>", unsafe_allow_html=True)  
            
                # Total PK Produced (kg)
                with col15_2:
                    st.session_state['yieldassess_TotalPKProduced'] = float((st.session_state['yieldassess_ProdKER'] / 100) * st.session_state['yieldassess_TotalWeight_PKRev'])
                    st.number_input('Total PK Produced (kg)', key='yieldassess_TotalPKProduced', disabled=True)

                with col15_3:
                    st.markdown('###')
                    st.markdown('### x')
            
                # PK Production Cost
                with col15_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_PKProdCost'] = float(ag['selected_rows'][0]['PK Production Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_PKProdCost']
                    st.number_input('PK Production Cost', key='yieldassess_PKProdCost', disabled=st.session_state['yieldassess_PKProdCost_disabled'])
            
                with col15_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total PK Production Cost
                with col15_6: 
                    st.session_state['yieldassess_TotalPKProdCost'] = format(float(st.session_state['yieldassess_TotalPKProduced']) * float(st.session_state['yieldassess_PKProdCost']), '.2f')
                    st.text_input('Total PK Production Cost', key='yieldassess_TotalPKProdCost', disabled=True)
            
            # Kandir Cost
            with st.container():
                with col16_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>Kandir Cost : </h4>", unsafe_allow_html=True)    
            
                # Total FFB Receipt
                with col16_2:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_KandirExp'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_KandirExp', disabled=True, format='%0.2f')  

                with col16_3:
                    st.markdown('###')
                    st.markdown('### x')
                    
                # Kandir Cost
                with col16_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_KandirCost'] = float(ag['selected_rows'][0]['Kandir Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_KandirCost']
                    st.number_input('Kandir Cost', key='yieldassess_KandirCost', disabled=st.session_state['yieldassess_KandirCost_disabled'])
            
                with col16_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total Kandir Cost
                with col16_6: 
                    st.session_state['yieldassess_TotalKandirCost'] = format(float(st.session_state['yieldassess_TotalWeight_KandirExp']) * float(st.session_state['yieldassess_KandirCost']), '.2f')
                    st.text_input('Total Kandir Cost', key='yieldassess_TotalKandirCost', disabled=True)   
                    
            # CPO Transport Cost
            with st.container():
                with col17_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>CPO Transport Cost : </h4>", unsafe_allow_html=True)         
                    
                # Total CPO Produced (kg)
                with col17_2:
                    st.session_state['yieldassess_TotalCPOProduced_TransCost'] = float((st.session_state['yieldassess_ProdOER'] / 100) * st.session_state['yieldassess_TotalWeight_CPORev'])
                    st.number_input('Total CPO Produced (kg)', key='yieldassess_TotalCPOProduced_TransCost', disabled=True)

                with col17_3:
                    st.markdown('###')
                    st.markdown('### x')  
                
                # CPO Transport Cost
                with col17_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_CPOTransCost'] = float(ag['selected_rows'][0]['CPO Transport Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_CPOTransCost']
                    st.number_input('CPO Transport Cost', key='yieldassess_CPOTransCost', disabled=st.session_state['yieldassess_CPOTransCost_disabled'])
            
                with col17_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total CPO Transport Cost
                with col17_6: 
                    st.session_state['yieldassess_TotalCPOTransCost'] = format(float(st.session_state['yieldassess_TotalCPOProduced_TransCost']) * float(st.session_state['yieldassess_CPOTransCost']), '.2f')
                    st.text_input('Total CPO Transport Cost', key='yieldassess_TotalCPOTransCost', disabled=True) 
                    
            # PK Transport Cost
            with st.container():
                with col18_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>PK Transport Cost : </h4>", unsafe_allow_html=True)         
                    
                # Total PK Produced (kg)
                with col18_2:
                    st.session_state['yieldassess_TotalPKProduced_TransCost'] = float((st.session_state['yieldassess_ProdKER'] / 100) * st.session_state['yieldassess_TotalWeight_PKRev'])
                    st.number_input('Total PK Produced (kg)', key='yieldassess_TotalPKProduced_TransCost', disabled=True)

                with col18_3:
                    st.markdown('###')
                    st.markdown('### x')  
                
                # PK Transport Cost
                with col18_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_PKTransCost'] = float(ag['selected_rows'][0]['PK Transport Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_PKTransCost']
                    st.number_input('PK Transport Cost', key='yieldassess_PKTransCost', disabled=st.session_state['yieldassess_PKTransCost_disabled'])
            
                with col18_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total PK Transport Cost
                with col18_6: 
                    st.session_state['yieldassess_TotalPKTransCost'] = format(float(st.session_state['yieldassess_TotalPKProduced_TransCost']) * float(st.session_state['yieldassess_PKTransCost']), '.2f')
                    st.text_input('Total PK Transport Cost', key='yieldassess_TotalPKTransCost', disabled=True)   
                    
                    
            # Shrinkage Cost 
            with st.container():
                with col19_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>Shrinkage Cost : </h4>", unsafe_allow_html=True)    
                    
                # Total FFB Receipt
                with col19_2:
                    if st.session_state['yieldassess_Status'] == '' and len(ag['selected_rows']) == 1:
                        st.session_state['yieldassess_TotalWeight_ShrinkageExp'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                    st.number_input('Total FFB Receipt (kg)', key='yieldassess_TotalWeight_ShrinkageExp', disabled=True, format='%0.2f')  

                with col19_3:
                    st.markdown('###')
                    st.markdown('### x')   
                
                # Shrinkage Cost
                with col19_4:
                    if st.session_state['yieldassess_Status'] == '':
                        st.session_state['yieldassess_ShrinkageCost'] = float(ag['selected_rows'][0]['Shrinkage Cost']) if len(ag['selected_rows']) == 1 else st.session_state['yieldassess_ShrinkageCost']
                    st.number_input('Shrinkage Cost', key='yieldassess_ShrinkageCost', disabled=st.session_state['yieldassess_ShrinkageCost_disabled'])
            
                with col19_5:   
                    st.markdown('###')
                    st.markdown('### =')
                    
                # Total Shrinkage Cost
                with col19_6: 
                    st.session_state['yieldassess_TotalShrinkageCost'] = format(float(st.session_state['yieldassess_TotalWeight_ShrinkageExp']) * float(st.session_state['yieldassess_ShrinkageCost']), '.2f')
                    st.text_input('Total Shrinkage Cost', key='yieldassess_TotalShrinkageCost', disabled=True)      
            
            # Total Expenses
            with st.container():
                with col20_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>Total Expenses : </h4>", unsafe_allow_html=True)
                with col20_2:
                    st.session_state['yieldassess_TotalExpenses'] = format(float(st.session_state['yieldassess_TotalAmount_Exp']) + 
                                                                        float(st.session_state['yieldassess_TotalCPOProdCost']) + 
                                                                        float(st.session_state['yieldassess_TotalPKProdCost']) + 
                                                                        float(st.session_state['yieldassess_TotalKandirCost']) +
                                                                        float(st.session_state['yieldassess_TotalCPOTransCost']) + 
                                                                        float(st.session_state['yieldassess_TotalPKTransCost']) +
                                                                        float(st.session_state['yieldassess_TotalShrinkageCost']), '.2f')
                    st.text_input('', key='yieldassess_TotalExpenses', disabled=True)       
            
            # Profit & Loss
            with st.container():
                with col21_1:
                    st.markdown('#####')
                    st.markdown("<h4 style='text-align: right;'>Profit & Loss : </h4>", unsafe_allow_html=True)
                    
                with col21_2:
                    st.session_state['yieldassess_ProfitAndLoss'] = format(float(st.session_state['yieldassess_TotalRevenue']) - 
                                                                        float(st.session_state['yieldassess_TotalExpenses']), '.2f')
                    st.text_input('', key='yieldassess_ProfitAndLoss', disabled=True)     
        
        
        
        
        # Supplier Pricing & OER Grid
        with tab2:
            
            # Export to excel
            col22_1, col22_2 = st.columns([15, 85])
            
            # Supplier Pricing & OER Grid
            col23_1, col23_2 = st.columns([60, 40])
            
            
            with st.container():
                with col23_1:
                    # Configure grid options using GridOptionsBuilder
                    if len(st.session_state['yieldassess_RecordList']) != 0 and len(ag['selected_rows']) == 1:
                       
                        Call_DisplaySupplierGridRecords(st.session_state['yieldassess_OUKey'], st.session_state['yieldassess_Date'])
                        
                        if len(st.session_state['yieldassess_SupplierList']) != 0:
                            builder2 = GridOptionsBuilder.from_dataframe(st.session_state['yieldassess_SupplierList'])
                            builder2.configure_pagination(enabled=False)
                            # builder2.configure_selection(selection_mode='single', use_checkbox=False)
                            builder2.configure_default_column(
                                resizable=True,
                                filterable=True,
                                sortable=True,
                                editable=False
                            )
                            builder2.configure_column(
                                field='FFBPrice',
                                header_name='FFB Unit Price',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='Weight',
                                header_name='Weight (kg)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='Amount',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            builder2.configure_column(
                                field='OER',
                                header_name='OER (%)',
                                type=["numericColumn", "numberColumnFilter", "customNumericFormat"],
                                precision=2
                            )
                            grid_options2 = builder2.build()

                            # Display AgGrid
                            ag2 = AgGrid(st.session_state['yieldassess_SupplierList'],
                                        gridOptions=grid_options2,
                                        editable=False,
                                        allow_unsafe_jscode=True,
                                        theme='balham',
                                        height=330,
                                        fit_columns_on_grid_load=True,
                                        reload_data=False,
                                        columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                        custom_css={
                                            '#gridToolBar': {
                                                'padding-bottom': '0px !important'
                                            }
                                        })
                    else:
                        st.session_state['yieldassess_SupplierList'] = []
                        
                        ag2 = AgGrid(pd.DataFrame([]),
                                    editable=False,
                                    allow_unsafe_jscode=True,
                                    theme='balham',
                                    height=300,
                                    fit_columns_on_grid_load=True,
                                    reload_data=False,
                                    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, # NO_AUTOSIZE (Default), FIT_ALL_COLUMNS_TO_VIEW, FIT_CONTENTS
                                    custom_css={
                                        '#gridToolBar': {
                                            'padding-bottom': '0px !important'
                                        }
                                    })  
                
                with st.container():
                    with col23_2:
                        # Average FFB Unit Price
                        if len(ag['selected_rows']) == 1:
                            st.session_state['yieldassess_AvgUnitPrice_Detail'] = float(ag['selected_rows'][0]['Average FFB Unit Price'])
                        st.number_input('Average FFB Unit Price', key='yieldassess_AvgUnitPrice_Detail', disabled=True, format='%0.6f')  

                        # Total Weight (kg)
                        if len(ag['selected_rows']) == 1:
                            st.session_state['yieldassess_TotalWeight_Detail'] = float(ag['selected_rows'][0]['Total FFB Receipt'])
                        st.number_input('Total Weight (kg)', key='yieldassess_TotalWeight_Detail', disabled=True, format='%0.2f')
                        
                        # Total Amount
                        if len(ag['selected_rows']) == 1:
                            st.session_state['yieldassess_TotalAmount_Detail'] = float(ag['selected_rows'][0]['Total FFB Procurement Amount'])
                        st.number_input('Total Amount', key='yieldassess_TotalAmount_Detail', disabled=True)    
                    
                        # OER (%)
                        if len(ag['selected_rows']) == 1:
                            st.session_state['yieldassess_OERBuying_Detail'] = float(ag['selected_rows'][0]['FFB Procurement OER'])
                        st.number_input('OER (%)', key='yieldassess_OERBuying_Detail', disabled=True, format='%0.2f')  
            
            with st.container():
                with col22_1:
                    if len(st.session_state['yieldassess_RecordList']) != 0 and len(ag['selected_rows']) == 1 and len(st.session_state['yieldassess_SupplierList']) != 0:
                        st.download_button(
                            "Download as excel",
                            data=to_excel(pd.DataFrame(st.session_state['yieldassess_SupplierList']).set_index('Crop Supplier')),
                            file_name="FFB Supplier Weight and OER.xlsx",
                            mime="application/vnd.ms-excel",
                            use_container_width=True
                        )
                    else:
                        st.markdown('#')    
                    
                    
                    
                    
                    
               
# def hide_MainPage():
#     placeholder.empty()
    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['yieldassess_Status'] == 'Submit':
            statusMsg.info(st.session_state['yieldassess_Message'])
        elif st.session_state['yieldassess_Status'] == 'New':
            statusMsg.success(st.session_state['yieldassess_Message'])
        elif st.session_state['yieldassess_Status'] == 'Edit':
            statusMsg.error(st.session_state['yieldassess_Message'])
            
def hide_StatusMsg():
    statusMsgSection.empty()
    

    
with pageSection:
    st.subheader('FFB Supplier Yield Assessment')
    statusMsg = st.empty()
    
    show_MainPage()
    
    # if st.session_state['yieldassess_Status'] == '':
    #     show_MainPage()
    #     hide_StatusMsg()
        # hide_Retry()
    # elif st.session_state['yieldassess_Status'] == 'Edit':
    #     hide_MainPage()
    #     show_StatusMsg()
    # elif st.session_state['yieldassess_Status'] == 'New':
    #     # hide_MainPage()
    #     show_StatusMsg()
        
        
