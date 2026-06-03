import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊")

st.title("📊 Analytics Dashboard")
st.write("Here is an example of rendering dynamic data and charts seamlessly.")

# Generate some dummy data
data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['Metrics A', 'Metrics B', 'Metrics C']
)

# Display a data table
st.subheader("Raw Data Summary")
st.dataframe(data.head())

# Display a line chart
st.subheader("Visualized Trends")
st.line_chart(data)