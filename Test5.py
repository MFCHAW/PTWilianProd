# import pandas as pd
# import streamlit as st

# data_df = pd.DataFrame(
#     {
#         "widgets": ["st.selectbox", "st.number_input", "st.text_area", "st.button"],
#         "favorite": [True, False, False, True],
#     }
# )

# st.data_editor(
#     data_df,
#     column_config={
#         "favorite": st.column_config.CheckboxColumn(
#             "Your favorite?",
#             help="Select your **favorite** widgets",
#             default=False,
#         )
#     },
#     disabled=["widgets"],
#     hide_index=True,
# )

import numpy as np
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

if 'pre_selected_rows' not in st.session_state:
    st.session_state.pre_selected_rows = []

df = pd.DataFrame(columns=['ID', 'STATUS'])
df['ID'] = [1, 2, 3]
df['STATUS'] = np.random.randint(0,100,size=(3))

# get pre-selected rows from session state
pre_selected_rows = st.session_state.pre_selected_rows

# use the pre-selected rows when building the grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection('multiple', pre_selected_rows=st.session_state.pre_selected_rows, use_checkbox=True)
gb_grid_options = gb.build()

# render the grid and get the selected rows
grid_return = AgGrid(
        df,
        gridOptions = gb_grid_options,
        key = 'ID',
        data_return_mode = DataReturnMode.AS_INPUT,
        update_mode = GridUpdateMode.MODEL_CHANGED, # GridUpdateMode.SELECTION_CHANGED or GridUpdateMode.VALUE_CHANGED or 
        height = 150,
        theme = "streamlit"
    )

if st.button("rerun"):
    st.experimental_rerun()