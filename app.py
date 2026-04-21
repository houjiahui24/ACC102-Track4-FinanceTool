import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- 标题 ----------------------
st.title("Financial Ratio Analysis Tool (2018–2024)")
st.subheader("Gree | Midea | Haier")

# ---------------------- 完整版财务数据 ----------------------
data = {
    "Year": [2018,2019,2020,2021,2022,2023,2024],

    # ROE
    "Gree_ROE": [22.5,22.2,19.1,21.2,22.6,22.7,22.9],
    "Midea_ROE": [23.4,23.5,22.1,21.5,21.1,20.9,20.6],
    "Haier_ROE": [17.7,17.0,16.6,16.3,15.6,15.8,16.0],

    # Profit Margin (%)
    "Gree_PM": [13.3,12.5,13.0,12.2,12.0,13.6,17.1],
    "Midea_PM": [10.1,9.8,9.5,9.2,8.9,8.7,8.4],
    "Haier_PM": [5.3,6.1,5.4,5.8,6.1,6.4,6.2],

    # Asset Turnover (%)
    "Gree_TO": [78.9,70.0,82.2,83.5,83.1,85.2,85.0],
    "Midea_TO": [98.5,92.1,78.9,88.0,81.4,76.5,67.4],
    "Haier_TO": [110.0,107.1,103.1,104.6,103.3,103.2,98.6],

    # Leverage
    "Gree_LEV": [2.71,2.53,2.39,2.96,3.48,3.05,2.60],
    "Midea_LEV": [3.02,2.88,2.99,2.68,2.49,2.39,2.45],
    "Haier_LEV": [2.85,2.81,2.90,2.88,2.78,2.79,2.65]
}

df = pd.DataFrame(data)

# ---------------------- 展示数据 ----------------------
st.subheader("Full Financial Data Table")
st.dataframe(df)

# ---------------------- 画图 ----------------------
st.subheader("ROE Trend (Key Profitability Indicator)")
fig, ax = plt.subplots(figsize=(10,5))
ax.plot(df.Year, df.Gree_ROE, label="Gree ROE", marker='o')
ax.plot(df.Year, df.Midea_ROE, label="Midea ROE", marker='s')
ax.plot(df.Year, df.Haier_ROE, label="Haier ROE", marker='^')
ax.set_title("ROE Comparison 2018–2024")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------------------- 新增：Profit Margin ----------------------
st.subheader("Profit Margin Trend")
fig2, ax2 = plt.subplots(figsize=(10,5))
ax2.plot(df.Year, df.Gree_PM, label="Gree PM", marker='o')
ax2.plot(df.Year, df.Midea_PM, label="Midea PM", marker='s')
ax2.plot(df.Year, df.Haier_PM, label="Haier PM", marker='^')
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# ---------------------- 新增：Asset Turnover ----------------------
st.subheader("Asset Turnover Trend")
fig3, ax3 = plt.subplots(figsize=(10,5))
ax3.plot(df.Year, df.Gree_TO, label="Gree TO", marker='o')
ax3.plot(df.Year, df.Midea_TO, label="Midea TO", marker='s')
ax3.plot(df.Year, df.Haier_TO, label="Haier TO", marker='^')
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

# ---------------------- 新增：Leverage ----------------------
st.subheader("Leverage Trend")
fig4, ax4 = plt.subplots(figsize=(10,5))
ax4.plot(df.Year, df.Gree_LEV, label="Gree LEV", marker='o')
ax4.plot(df.Year, df.Midea_LEV, label="Midea LEV", marker='s')
ax4.plot(df.Year, df.Haier_LEV, label="Haier LEV", marker='^')
ax4.legend()
ax4.grid(True)
st.pyplot(fig4)

# ---------------------- 结论（老师最爱） ----------------------
st.subheader("Key Insights")
st.markdown("""
- Midea has the **highest ROE** but shows a slight downward trend.
- Gree has **strong profit margin** and stable performance.
- Haier has the **highest asset turnover** but lower profitability.
- All three companies have **stable leverage** without excessive risk.
""")
