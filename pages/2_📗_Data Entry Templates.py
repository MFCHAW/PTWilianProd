import streamlit as st
from streamlit_extras.switch_page_button import switch_page

if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()

st.title('Data Entry Template')

# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


st.markdown('''
    ## Spreadsheet Links:
    ### A) Daily Pricing:
    #### 1. [Libo - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/Libo_FFB%20Daily%20Pricing.xlsx?d=wef3f86df1dd34f8bbf5ae08d84ab71f5&csf=1&web=1&e=2DhGp8)
    #### 2. [SSP1 - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP1_FFB%20Daily%20Pricing.xlsx?d=w3075a5e13f4142b8be39d3361549243d&csf=1&web=1&e=mhyEdA)
    #### 3. [SSP2 - FFB Daily Pricing](https://lintramaxmy.sharepoint.com/:x:/r/sites/LMShared/Shared%20Documents/Wilian%20Perkasa/FFB%20Procurement%20Live%20Templates/SSP2_FFB%20Daily%20Pricing.xlsx?d=wd1d318dc86bc4bb69331d345a9289ef5&csf=1&web=1&e=tBSxG4)
''')
