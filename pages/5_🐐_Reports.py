import streamlit as st

st.title('Reports')

# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

reportList = ['Daily FFB Proceeds', 'FFB Proceeds Summary',
              'FFB Proceeds Detail', 'FFB Proceeds Statement']

selectbox1 = st.sidebar.selectbox(
    'Please select a report: ',
    (reportList)
)
