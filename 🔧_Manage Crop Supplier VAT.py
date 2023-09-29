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
if 'manageVAT_OUKey' not in st.session_state:
    st.session_state['manageVAT_OUKey'] = -1

if 'manageVAT_SupplierList' not in st.session_state:
    st.session_state['manageVAT_SupplierList'] = []


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



# -- Get Operating Unit Lookup Records --
def lookup_OperatingUnit():
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select OUKey, OUCode, OUDesc
                           from GMS_OUStp
                           Where OperationTypeKey = 3""")
        
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

# -- Get Operating Unit Key --
def get_OUKey(ou):
    
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select OUKey
                           from GMS_OUStp
                           Where OperationTypeKey = 3 and OUCode + ' - ' + OUDesc = '{ou}'""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['manageVAT_OUKey'] = df['OUKey'].iloc[0]
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
           
            
def get_CropSuplierList(oukey):
    conn = qconnection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""select EstateCode as [Code], 
                                EstateDesc as [Supplier],
                                PPNType as [VAT Type],
                                IsPPNInPymt as [Include in Payment]
                           from GMS_EstateStp
                           where EstateKey <> -1 and Active = 1
                                 and OUKey =  '{oukey}'""")
                
        result = []
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            result.append(dict(zip(columns, row)))

        df = pd.DataFrame(result)
        
        st.session_state['manageVAT_SupplierList'] = df
        
    except pymssql.Error as e:
        st.write(f'Error executing query: {e}')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    


# -- UI Session --
def show_MainPage():
    with placeholder.container():
        ou = st.selectbox(
            'Mill: ',
            lookup_OperatingUnit()
        )
        
        get_OUKey(ou)
        
        get_CropSuplierList(st.session_state['manageVAT_OUKey'])
        
        st.markdown('#')
        
        with st.container():
            left_column, right_column = st.columns((1, 2))
            
            with left_column:
                # Configure grid options using GridOptionsBuilder
                builder = GridOptionsBuilder.from_dataframe(st.session_state['manageVAT_SupplierList'])
                builder.configure_pagination(enabled=False)
                builder.configure_selection(selection_mode='single', use_checkbox=False)
                grid_options = builder.build()

                # Display AgGrid
                st.write("Crop Supplier Listing: ")
                # st.table(st.session_state['manageVAT_SupplierList'])
                ag = AgGrid(st.session_state['manageVAT_SupplierList'],
                            gridOptions=grid_options,
                            editable=False,
                            allow_unsafe_jscode=True,
                            theme='balham',
                            height=500,
                            fit_columns_on_grid_load=True,
                            reload_data=False)
                
            with right_column:
                code = st.text_input('Code', value=ag['selected_rows'][0]['Code'] if len(ag['selected_rows']) == 1 else '', disabled=True)
                supplier = st.text_input('Supplier', value=ag['selected_rows'][0]['Supplier'] if len(ag['selected_rows']) == 1 else '', disabled=True)
            
                print(ag['selected_rows'][0]['VAT Type'])
            
                vat = st.selectbox(
                            'VAT Type: ',
                            options=['', 'PPN', 'PPNPUT'],
                            index=1
                            #ag['selected_rows'][0]['VAT Type'] if len(ag['selected_rows']) == 1 else ''
                            #on_change=ag['selected_rows'][0]['VAT Type'] if len(ag['selected_rows']) == 1 else ''
                        )
        
        


with pageSection:
    st.title('Manage Crop Supplier VAT')
    statusMsg = st.empty()
    
    show_MainPage()
    
    
    
    
    
