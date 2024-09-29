import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

with st.form("user_input_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    submit_button = st.form_submit_button("Submit")
    
    if submit_button:
        st.write(f"Username: {username}")
        st.write(f"Email: {email}")
        
x = st.slider('x') # this is a widget
st.write(x, 'squared is', x * x)        