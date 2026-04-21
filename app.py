import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("ACC102 Financial Ratio Analyzer")
st.subheader("ROE Analysis: Gree, Midea, Haier (2018–2024)")

# 数据
data = {
    "Year": [2018,2019,2020,2021,2022,2023,2024],
    "Gree_ROE": [22.5,22.2,19.1,21.2,22.6,22.7,22.9],
    "Midea_ROE": [23.4,23.5,22.1,21.5,21.1,20.9,20.6],
    "Haier_ROE": [17.7,17.0,16.6,16.3,15.6,15.8,16.0]
}
df = pd.DataFrame(data)

# 展示数据
st.subheader("Data Table")
st.dataframe(df)

# 画图
st.subheader("ROE Trend")
st.line_chart(df.set_index("Year"))

# 结论
st.subheader("Key Insights")
st.write("✅ Midea has the highest & most stable ROE")
st.write("✅ Gree maintains strong profitability")
st.write("✅ Haier is steady but lower")
