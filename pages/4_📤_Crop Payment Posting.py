import streamlit as st
from streamlit_extras.switch_page_button import switch_page
# import time

if 'loggedIn' not in st.session_state:
    st.session_state['loggedIn'] = False

if st.session_state['loggedIn'] == False:
    switch_page('Home')
    st.stop()

st.title('Crop Payment Posting')

# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)

st.markdown('#')

with st.form(key='cropPayment'):
    ou = st.selectbox(
        'Mill: ',
        ('LIBO SAWIT PERKASA PALM OIL MILL',
            'SEMUNAI SAWIT PERKASA PALM OIL MILL 1',
            'SEMUNAI SAWIT PERKASA PALM OIL MILL 2')
    )

    batch = st.number_input('Batch: ', 1)

    st.markdown('#')

    computePayment = st.form_submit_button(label='Post Payment')

    st.markdown('#')

    st.write('Please fill in all the information and click "Post Payment" button.')


# with st.empty():
#     for seconds in range(60):
#         st.write(f"⏳ {seconds} seconds have passed")
#         time.sleep(1)
#     st.write("✔️ 1 minute over!")
