import streamlit as st

st.header("Container")
chk1 = st.checkbox(label="Trigger Text change")

container = st.container()

with st.container():
    st.write("This is inside the container 1")

with st.container():
    st.write("This is inside the container 2")

if chk1:
    container.write("First Choice")
else:
    container.write("Second Choice")
