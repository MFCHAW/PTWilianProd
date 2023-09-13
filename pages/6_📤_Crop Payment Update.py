import streamlit as st
import pandas as pd
import pymssql
import json
import asyncio
import aiohttp

from streamlit_extras.switch_page_button import switch_page
from st_aggrid import AgGrid, GridOptionsBuilder

from init_connection import qconnection


# -- Variables and Session States Initialization --
if 'updatePrice_status' not in st.session_state:
    st.session_state['updatePrice_status'] = ''
    
if 'updatePrice_message' not in st.session_state:
    st.session_state['updatePrice_message'] = ''

if 'updatePrice_error_message' not in st.session_state:
    st.session_state['updatePrice_error_message'] = pd.DataFrame()
    
if 'updatePrice_EstateCode' not in st.session_state:
    st.session_state['updatePrice_EstateCode'] = ''
    
if 'updatePrice_EstateDesc' not in st.session_state:
    st.session_state['updatePrice_EstateDesc'] = ''

if 'updatePrice_OUKey' not in st.session_state:
    st.session_state['updatePrice_OUKey'] = -1
    
if 'updatePrice_OUKey' not in st.session_state:
    st.session_state['updatePrice_OUKey'] = 0
    
if 'updatePrice_TemplateName' not in st.session_state:
    st.session_state['updatePrice_TemplateName'] = ''
    
url = st.secrets['url_PriceUpdating']


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
errorMsgSection = st.container()
retrySection = st.container()



# -- Get Operating Unit Key --
def get_OUKey(ou):
    
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select OUKey
                           from GMS_OUStp
                           Where Active = 1 and OperationTypeKey = 3 and OUCode + ' - ' + OUDesc = '{ou}'""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['updatePrice_OUKey'] = df['OUKey'].iloc[0]
        
        if st.session_state['updatePrice_OUKey'] == 6:
            st.session_state['updatePrice_TemplateName'] = 'Libo_FFB Daily Pricing.xlsx'
        elif st.session_state['updatePrice_OUKey'] == 8:
            st.session_state['updatePrice_TemplateName'] = 'SSP1_FFB Daily Pricing.xlsx'
        elif st.session_state['updatePrice_OUKey'] == 9:
            st.session_state['updatePrice_TemplateName'] = 'SSP2_FFB Daily Pricing.xlsx'
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -- Get Crop Supplier Code --
def get_EstateCode(supplier):
    
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select EstateCode, EstateDesc
                           from GMS_EstateStp
                           Where EstateCode + ' - ' + EstateDesc = '{supplier}'""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['updatePrice_EstateCode'] = df['EstateCode'].iloc[0]
        st.session_state['updatePrice_EstateDesc'] = df['EstateDesc'].iloc[0]
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            

# -- Get Batch No. --
def get_Batch(batch):
    
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""Select d.FPSBatchCode
                           from FPS_FinalPayDet a 
                                LEFT OUTER JOIN FPS_FFBApplyPaymentDet b on a.FFBApplyPaymentDetKey = b.FFBApplyPaymentDetKey 
                                INNER JOIN FPS_FFBApplyPaymentHdr c on b.FFBApplyPaymentHdrKey = c.FFBApplyPaymentHdrKey 
                                LEFT OUTER JOIN FPS_MthEndClose d on c.FPSBatchKey = d.FPSBatchKey 
                                LEFT OUTER JOIN GMS_EstateStp e ON b.ContactKey = e.ContactKey
                           Where 'Batch: ' + d.FPSBatchCode + ' (' + Convert(varchar(10), d.FromDate, 103) + ' - ' + Convert(varchar(10), d.ToDate, 103) + ')' = '{batch}'""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['updatePrice_Batch'] = df['FPSBatchCode'].iloc[0]
        
        # print(st.session_state['updatePrice_Batch'])
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
    
    
# -- Get Operating Unit Lookup Records --
def lookup_OperatingUnit():
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select OUKey, OUCode, OUDesc
                           from GMS_OUStp
                           Where Active = 1 and OperationTypeKey = 3""")
        
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        return df['OUCode'] + ' - ' + df['OUDesc']
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# -- Get Crop Supplier Lookup Records --
def lookup_CropSupplier(ou):
    conn = qconnection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"""select EstateCode, EstateDesc
                           from GMS_EstateStp
                           where EstateKey <> -1 and Active = 1 and OUKey = {st.session_state['updatePrice_OUKey']}""")
        
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        return df['EstateCode'] + ' - ' + df['EstateDesc']
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
# -- Get Batch Lookup Records --
def lookup_Batch():
    conn = qconnection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(f"""Select d.FPSBatchCode, d.FromDate, d.ToDate 
                            from FPS_FinalPayDet a 
                                 LEFT OUTER JOIN FPS_FFBApplyPaymentDet b on a.FFBApplyPaymentDetKey = b.FFBApplyPaymentDetKey 
                                 INNER JOIN FPS_FFBApplyPaymentHdr c on b.FFBApplyPaymentHdrKey = c.FFBApplyPaymentHdrKey 
                                 LEFT OUTER JOIN FPS_MthEndClose d on c.FPSBatchKey = d.FPSBatchKey 
                                 LEFT OUTER JOIN GMS_EstateStp e ON b.ContactKey = e.ContactKey
                            where a.FinalPayDetKey <> -1 and c.OUKey = {st.session_state['updatePrice_OUKey']} and e.EstateCode = '{st.session_state['updatePrice_EstateCode']}'""")
        
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        if df.shape[0] == 0:
            return ''
        else:
            return 'Batch: ' + df['FPSBatchCode'] + ' (' + df['FromDate'].dt.strftime("%d/%m/%Y") + ' - ' + df['ToDate'].dt.strftime("%d/%m/%Y") + ')'
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            

# -- Trigger Azure Logic App to update the crop supplier payment --
async def updatePricing(ou, estateCode, batch):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "OUKey": str(st.session_state['updatePrice_OUKey']),
            "EstateCode": st.session_state['updatePrice_EstateCode'],
            "FPSBatchCode": str(st.session_state['updatePrice_Batch']),
            "PriceExcelName": st.session_state['updatePrice_TemplateName'],
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            # print(data)

            # -- Check the ErrorList table got records. --
            # -- If got record, system show error and return the error records --
            conn = qconnection()
            cursor = conn.cursor()
            
            try:
                cursor.execute(f"""Select a.ErrorMsgDT as [Date Time], b.OUDesc as [Oil Mill], 
                                          FPSBatchCode as [Batch No.], ErrorMsg as [Error Message] 
                                   from FPS_YYT_BatchErrorList a left join GMS_OUStp b on a.OUKey = b.OUKey
                                   Where a.OUKey = {st.session_state['updatePrice_OUKey']} and a.FPSBatchCode = '{st.session_state['updatePrice_Batch']}' and  
                                         ProcessType = 'MAINT'""")
                
                result = []
                columns = [column[0] for column in cursor.description]
                for row in cursor.fetchall():
                    result.append(dict(zip(columns, row)))

                df = pd.DataFrame(result)
                st.session_state['updatePrice_error_message'] = df
                # print(df)
                
            except pymssql.Error as e:
                st.write(f'Error executing query: {e}')
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
            
            # if response.status == 200 and data['Status'] != 'Failed' and len(result) == 0:
            if len(result) == 0:
                st.session_state['updatePrice_status'] = 'Succeeded'
                st.session_state['updatePrice_message'] = f'''{st.session_state['updatePrice_EstateCode']} - {st.session_state['updatePrice_EstateDesc']} payments already being updated!'''
            else:
                st.session_state['updatePrice_status'] = 'Failed'
                st.session_state['updatePrice_message'] = f'''Error occured during crop payment updating for {st.session_state['updatePrice_EstateCode']} - {st.session_state['updatePrice_EstateDesc']}!'''


def updatePrice(ou, supplier, batch):
    
    st.session_state['updatePrice_status'] = 'Process'
    st.session_state['updatePrice_message'] = 'Crop payment updating in progress...'
    
    hide_MainPage()
    show_StatusMsg()
    hide_ErrorMsg() 
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(updatePricing({st.session_state['updatePrice_OUKey']}, {st.session_state['updatePrice_EstateCode']}, {st.session_state['updatePrice_Batch']})) 
    
    # time.sleep(3) 
    # st.session_state['posting_status'] = 'Succeeded'
    # st.session_state['posting_message'] = 'All related payments already being posted!'
    
    st.markdown('#')


# -- UI Session --
def show_MainPage():
    with placeholder.container():
        if st.session_state['updatePrice_status'] == '':
            ou = st.selectbox(
                'Mill: ',
                lookup_OperatingUnit()
            )
            
            get_OUKey(ou)
            
            supplier = st.selectbox(
                'Crop Supplier: ',
                lookup_CropSupplier(ou)
            )
            
            get_EstateCode(supplier)
            
            batch = st.selectbox(
                'Batch: ',
                lookup_Batch()
            )
            
            get_Batch(batch)

            st.markdown('#')

            st.button('Update Payment',
                    on_click=updatePrice,
                    args=(st.session_state['updatePrice_OUKey'], st.session_state['updatePrice_EstateCode'], batch),
                    help='Click to start the payment posting.')

            st.markdown('#')

            st.write('Please fill in all the information and click "Update Payment" button.')

def hide_MainPage():
    placeholder.empty()
    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['updatePrice_status'] == 'Process':
            statusMsg.info(st.session_state['updatePrice_message'])
        elif st.session_state['updatePrice_status'] == 'Succeeded':
            statusMsg.success(st.session_state['updatePrice_message'])
        elif st.session_state['updatePrice_status'] == 'Failed':
            statusMsg.error(st.session_state['updatePrice_message'])

def hide_StatusMsg():
    statusMsgSection.empty()
    
def show_ErrorMsg():
    with errorMsgSection:
        if st.session_state['updatePrice_error_message'].any().any():
            # Configure grid options using GridOptionsBuilder
            builder = GridOptionsBuilder.from_dataframe(st.session_state['updatePrice_error_message'])
            builder.configure_pagination(enabled=False)
            builder.configure_selection(selection_mode='single', use_checkbox=False)
            grid_options = builder.build()

            # Display AgGrid
            st.write("Error Details: ")
            st.table(st.session_state['updatePrice_error_message'])
            # ag = AgGrid(st.session_state['pricing_error_message'],
            #         gridOptions=grid_options,
            #         editable=False,
            #         allow_unsafe_jscode=True,
            #         theme='balham',
            #         height=500,
            #         fit_columns_on_grid_load=True,
            #         reload_data=False)
    
def hide_ErrorMsg():
    errorMsgSection.empty()
    
def hide_Retry():
    retrySection.empty()
    
def show_Retry():
    with retrySection:
        st.button('Retry',
                    on_click=reset_Form,
                    help='Click to retry.')
        
def reset_Form():
    st.session_state['updatePrice_status'] = ''
    st.session_state['updatePrice_message'] = ''
    st.session_state['updatePrice_error_message'] = ''
            

with pageSection:
    st.title('Update Crop Payment')
    statusMsg = st.empty()
    
    if st.session_state['updatePrice_status'] == '':
        show_MainPage()
        hide_StatusMsg()
        hide_ErrorMsg()
        hide_Retry()
    elif st.session_state['updatePrice_status'] == 'Succeeded':
        hide_MainPage()
        show_StatusMsg()
        hide_ErrorMsg()
        show_Retry()
    elif st.session_state['updatePrice_status'] == 'Failed':
        hide_MainPage()
        show_StatusMsg()
        show_ErrorMsg()
        show_Retry()
