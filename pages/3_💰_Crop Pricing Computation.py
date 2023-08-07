import streamlit as st
import asyncio
import aiohttp
import json
from streamlit_javascript import st_javascript
from streamlit_extras.switch_page_button import switch_page

if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()


def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url('https://lmquartobistorage.blob.core.windows.net/pt-wilian-perkasa/PTWP_Logo.png');
                background-repeat: no-repeat;
                padding-top: 10px;
                background-position: 20px 20px;
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

st.title('Crop Price Computation')

# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

placeholder = st.empty()


url = 'https://prod-37.southeastasia.logic.azure.com:443/workflows/8d3ee9a9b3bc46868eca0b23032e7c13/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9TAwgb1TlIaN5SBi40BSN6S87LDXZSxY5Iniz1N-ND8'


async def processPricing(ou, year, month):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps({
            "OU": ou,
            "Year": year,
            "Month": month
        }, sort_keys=True), headers={'content-type': 'application/json'}) as response:
            data = await response.json()
            st.write(data)

            if response.status == 200:
                st.session_state['g_message'] = 'Pricing computation done!'
                statusMsg.text(st.session_state['g_message'])
            else:
                st.session_state['g_message'] = 'Error occured during pricing computation!'
                statusMsg.text(st.session_state['g_message'])

with placeholder.container():
    with st.form(key='cropPrice'):
        ou = st.selectbox(
            'Mill: ',
            ('LIBO SAWIT PERKASA PALM OIL MILL',
                'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
                'SEMUNAI SAWIT PERKASA PALM OIL MILL 2')
        )

        year = st.selectbox(
            'Year: ',
            ('2023', '2024')
        )

        month = st.selectbox(
            'Month: ',
            ('January',
                'February',
                'March',
                'April',
                'May',
                'June',
                'July',
                'August',
                'September',
                'October',
                'November',
                'December'),
            8
        )

        st.markdown('#')

        computePrice = st.form_submit_button(label='Process',
                                             help='Click to start process the pricing.')

        st.markdown('#')

        st.write('Please fill in all the information and click "Process" button.')


statusMsg = st.empty()

if computePrice:
    placeholder.empty()
    st.session_state['g_message'] = 'Processing...'
    statusMsg.text(st.session_state['g_message'])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(processPricing(ou, year, month))
