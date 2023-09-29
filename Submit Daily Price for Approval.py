import streamlit as st
import pandas as pd
import pymssql
import json
import asyncio
import aiohttp


from streamlit_extras.switch_page_button import switch_page
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

from init_connection import qconnection


# -- Variables and Session States Initialization --
if 'submitPricing_OUKey' not in st.session_state:
    st.session_state['submitPricing_OUKey'] = -1
    
if 'submitApprove_Year' not in st.session_state:
    st.session_state['submitPricing_Year'] = 1900
    
if 'submitPricing_Month' not in st.session_state:
    st.session_state['submitPricing_Month'] = 1
    
if 'submitPricing_DayList' not in st.session_state:
    st.session_state['submitPricing_DayList'] = []
    
if 'submitPricing_UpdatedRecords' not in st.session_state:
    st.session_state['submitPricing_UpdatedRecords'] = {}
    
if 'submitPricing_status' not in st.session_state:
    st.session_state['submitPricing_status'] = ''

if 'submitPricing_message' not in st.session_state:
    st.session_state['submitPricing_message'] = ''


url = st.secrets['url_submitPricing']



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
# errorMsgSection = st.container()
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
        
        st.session_state['submitPricing_OUKey'] = df['OUKey'].iloc[0]
        
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
            
            
# -- Get Year Lookup Records --
def lookup_Year(oukey):
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select Distinct Yr
                           from FPS_YYT_FFBDailyPriceList
                           where oukey = '{oukey}'""")
        
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['submitPricing_Year'] = df['Yr'].iloc[0]
        
        return df['Yr']
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
            
# -- Get Month Lookup Records --
def lookup_Month(oukey, year):
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select Distinct Mth
                           from FPS_YYT_FFBDailyPriceList
                           where oukey = '{oukey}' and Yr = '{year}'""")
        
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['submitPricing_Month'] = df['Mth'].iloc[0]
        
        return df['Mth']
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
           
           
def get_DayList(oukey, year, month):
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""with temptbl as (
                            select Distinct Convert(date, RateDate, 103) as Date
                            from FPS_YYT_FFBDailyPriceList
                            where oukey = {oukey} and Yr = {year} and Mth = {month}
                                  and (Convert(varchar, OUKey) + '-' + Convert(varchar, Yr) + '-' + Convert(varchar, Mth) + Convert(varchar, Convert(date, RateDate, 103)) Not In (
                                        Select Convert(varchar, OUKey) + '-' + Convert(varchar, Yr) + '-' + Convert(varchar, Mth) + Convert(varchar, Convert(date, RateDate, 103))
                                        From FPS_YYT_AppFFBDailyPriceList
                                        Where oukey = {oukey} and Yr = {year} and Mth = {month}
                                        ))
                            )
                            Select 'False' as [Select], Date 
                            From temptbl
                            Order By Date""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['submitPricing_DayList'] = df
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            

def hide_MainPage():
    placeholder.empty()  
    
def show_StatusMsg():
    with statusMsgSection:
        statusMsg.empty()
        
        if st.session_state['submitPricing_status'] == 'Submitted':
            statusMsg.success(st.session_state['submitPricing_message'])
       

def hide_StatusMsg():
    statusMsgSection.empty()
    
def reset_Form():
    st.session_state['submitPricing_status'] = ''
    st.session_state['submitPricing_message'] = ''
    
def hide_Retry():
    retrySection.empty()
    
def show_Retry():
    with retrySection:
        st.button('Retry',
                    on_click=reset_Form,
                    help='Click to retry.')
        

# -- Trigger Azure Logic App to submit Approval for Daily Pricing --
async def submitPricing(oukey, year, month, data):
    session_timeout = aiohttp.ClientTimeout(total=60 * 60 * 24)
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
        async with session.post(url, data=json.dumps({
            "OUKey": str(oukey),
            "Year": str(year),
            "Month": str(month),
            # "Data": str(data.to_json(date_format="iso",orient='records')[1:-1].replace('},{', '} {')),
            "Data": data
            "UserKey": st.session_state['UserKey']
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()

            if response.status == 200 and data['Status'] != 'Failed':
                st.session_state['submitPricing_status'] = 'Succeeded'
                st.session_state['submitPricing_message'] = 'Daily crop supplier pricing already submitted for approval!'
            else:
                st.session_state['submitPricing_status'] = 'Failed'
                st.session_state['submitPricing_message'] = 'Error occured during daily crop supplier pricing submition!'
    
            
def submitPriceApprove(oukey, year, month, data):
    
    st.session_state['submitPricing_status'] = 'Submitted'
    st.session_state['submitPricing_message'] = 'Submitted for approval.'
    
    hide_MainPage()
    show_StatusMsg()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(submitPricing(oukey, year, month, data)) 
    
    # conn = qconnection()
    # cursor = conn.cursor()

    # try:
    #     cursor.execute(f"""select OUKey, Yr, Mth, EstateCode, EstateDesc, SuppCatCode, RateDate, Rate 
    #                         from FPS_YYT_FFBDailyPriceList
    #                         Where OUKey = {oukey} and Yr = {year} and Mth = {month}""")
                
    #     result = []
    #     columns = [column[0] for column in cursor.description]
    #     for row in cursor.fetchall():
    #         result.append(dict(zip(columns, row)))

    #     df1 = pd.DataFrame(result)
        
    #     df2 = st.session_state['submitApprove_UpdatedRecords'][(st.session_state['submitApprove_UpdatedRecords'].Select == "True")]
        
    #     json = df1[(df1.RateDate.isin(df2.Date))].to_json(date_format="iso",orient='records')[1:-1].replace('},{', '} {')
        
    #     st.write(json)
        
    #     # for index, row in df1[(df1.RateDate.isin(df2.Date))].iterrows():
    #     #     cursor.execute("INSERT INTO FPS_YYT_AppFFBDailyPriceList (OUKey, Yr, Mth, EstateCode, EstateDesc, SuppCatCode, RateDate, Rate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (row.OUKey, row.Yr, row.Mth, row.EstateCode, row.EstateDesc, row.SuppCatCode, row.RateDate, row.Rate))
            
    #     # conn.commit()
        
    # except pymssql.Error as e:
    #     st.write(f'Error executing query: {e}')
    # finally:
    #     if cursor:
    #         cursor.close()
    #     if conn:
    #         conn.close()
    
    
# -- UI Session --
def show_MainPage():
    with placeholder.container():
        if st.session_state['submitPricing_status'] == '':
            ou = st.selectbox(
                'Mill: ',
                lookup_OperatingUnit()
            )
            
            get_OUKey(ou)
            
            year = st.selectbox(
                'Year: ',
                lookup_Year(st.session_state['submitPricing_OUKey'])
            )
            
            month = st.selectbox(
                'Month: ',
                lookup_Month(st.session_state['submitPricing_OUKey'], st.session_state['submitPricing_Year'])
            )
            
            get_DayList(st.session_state['submitPricing_OUKey'], st.session_state['submitPricing_Year'], st.session_state['submitPricing_Month'])
            
            st.markdown('#')
            
            with st.container():
                left_column, right_column = st.columns((1, 2))
            
                with left_column:
                    st.write("Please tick the day's to submit for approval: ")
                    
                    st.session_state['submitApprove_UpdatedRecords'] = st.data_editor(
                                                                            st.session_state['submitPricing_DayList'],
                                                                            column_config={
                                                                                "Select": st.column_config.CheckboxColumn(
                                                                                    "Submit thsi date?",
                                                                                    help="Choose the date.",
                                                                                    default=False,
                                                                                )
                                                                            },
                                                                            disabled=["widgets"],
                                                                            hide_index=True,
                                                                        )
                    
                    st.write(st.session_state['submitApprove_UpdatedRecords'][(st.session_state['submitApprove_UpdatedRecords'].Select == "True")])
                    
                with right_column:
                    st.markdown('#')
                    st.markdown('#')
                    st.button('Submit',
                            on_click=submitPriceApprove,
                            args=(st.session_state['submitPricing_OUKey'], 
                                  st.session_state['submitPricing_Year'], 
                                  st.session_state['submitPricing_Month'],
                                  st.session_state['submitApprove_UpdatedRecords'][(st.session_state['submitApprove_UpdatedRecords'].Select == "True")]),
                            help='Click to submit the selected daily pricing for approval.')
            
        st.write('Please fill in all the information and click "Submit" button.')

with pageSection:
    st.title('Submit Daily Price for Approval')
    statusMsg = st.empty()
    
    if st.session_state['submitPricing_status'] == '':
        show_MainPage()
        hide_StatusMsg()
        hide_Retry()
    elif st.session_state['submitPricing_status'] == 'Submitted':
        hide_MainPage()
        show_StatusMsg()
        show_Retry()