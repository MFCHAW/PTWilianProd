import streamlit as st
from common import set_page_container_style

# --- Define page configuration ---
st.set_page_config(
    page_title='PT Wilian - FFB Procurement',
    page_icon='✍',
    initial_sidebar_state='collapsed',
    layout='wide'
)

# set_page_container_style(
#     max_width=1100, max_width_100_percent=True,
#     padding_top=0, padding_right=10, padding_left=5, padding_bottom=10
# )


st.sidebar.title('FFB Procurement')

# st.sidebar.success('Select a page above.')


# Adding additional controls in the sidebar.
# Using object notation
add_selectbox = st.sidebar.selectbox(
    'How would you like to contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# if 'g_message' in st.session_state:
#     st.text(st.session_state['g_message'])

# Using 'with' notation
with st.sidebar:
    add_radio = st.radio(
        'Choose a shipping method',
        ('Standard (5-15 days)', 'Express (2-5 days)')
    )

# Page Title
st.title('Dashboard')


# --- Hide the Streamlit Menu Button and Trade Marks ---
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


# # Temporary store the input into the memory and share with other pages.abs
# if 'my_input' not in st.session_state:
#     st.session_state['my_input'] = ''

# my_input = st.text_input('Input a text here', st.session_state['my_input'])
# submit = st.button('Submit')

# if submit:
#     st.session_state['my_input'] = my_input
#     st.write('You have entered:', my_input)
