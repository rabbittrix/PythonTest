import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generate_data(num_rows):
    data = {
        'A': np.random.randn(num_rows),
        'B': np.random.randn(num_rows),
        'C': np.random.rand(num_rows)
    }
    
    return pd.DataFrame(data)

# Streamlit configuration theme
st.set_page_config(
    page_title='Data Visualization with Streamlit',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded'
)

st.markdown("""
    <style>
    .fixed-slider {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        background: #282a36;
        z-index: 1000;
        padding: 10px 0;
        margin: 0;
    }
    .slider-container {
        padding: 10px;
        background-color: #282a36;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('POC for Data Visualization with Streamlit')

st.markdown('<div class="fixed-slider"><div class="slider-container">', unsafe_allow_html=True)
num_rows = st.slider('Number of rows', min_value=10, max_value=1000, value=100)
st.markdown('</div></div>', unsafe_allow_html=True)

df = generate_data(num_rows)

st.subheader('Data Table')
st.write(df)

st.subheader('Data Plots')

fig, ax = plt.subplots()
df[['A', 'B']].plot(ax=ax)
ax.set_title('Line Plot of A and B')
st.pyplot(fig)

fig, ax = plt.subplots()
df['C'].plot(kind='hist', ax=ax, bins=30)
ax.set_title('Histogram of C')
st.pyplot(fig)

st.write('Graphs and data updated based on the selected number of rows')