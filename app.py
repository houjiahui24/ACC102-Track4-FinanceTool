import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ACC102 Dashboard", layout="wide")
st.title("📊 ACC102 Track4 - Financial Analysis Tool")
st.caption("Data Source: WRDS Compustat 2010–2024")

# ----------------------
# 直接用示例数据，不连WRDS
# ----------------------
data = {
    "tic": ["AAPL","AAPL","MSFT","MSFT","GOOGL","GOOGL","AMZN","AMZN","NVDA","NVDA"],
    "year": [2020,2023,2020,2023,2020,2023,2020,2023,2020,2023],
    "roe": [60,70,40,48,20,25,15,22,50,75],
    "roa": [18,22,15,18,12,14,8,10,20,28],
    "lev": [0.7,0.65,0.6,0.58,0.5,0.48,0.7,0.69,0.5,0.45],
    "sale": [270,380,140,210,180,280,380,510,100,400]
}
df = pd.DataFrame(data)

# 侧边栏筛选
companies = st.sidebar.multiselect(
    "Choose Companies",
    ["AAPL","MSFT","GOOGL","AMZN","NVDA"],
    default=["AAPL","MSFT","NVDA"]
)
df = df[df["tic"].isin(companies)]

# 展示
st.subheader("Data Table")
st.dataframe(df.round(2))

# 图表1 ROE
st.subheader("ROE Trend")
fig, ax = plt.subplots(figsize=(10,4))
for c in companies:
    d = df[df["tic"]==c]
    ax.plot(d["year"], d["roe"], marker="o", label=c)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# 图表2 收入
st.subheader("Revenue Comparison")
rev = df.pivot(index="year", columns="tic", values="sale")
st.bar_chart(rev)
