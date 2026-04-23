import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

@st.cache_data
def load_data():
    df = pd.read_csv("wrds_data.csv")
    # 计算财务指标
    df['roe'] = df['ni'] / df['ceq']
    df['roa'] = df['ni'] / df['at']
    df['pm'] = df['ni'] / df['sale']
    df['lev'] = df['at'] / df['ceq']
    return df

df = load_data()

# 侧边栏筛选
st.sidebar.header("Settings")
companies = st.sidebar.multiselect(
    "Companies",
    df["tic"].unique(),
    default=df["tic"].unique()
)

# 这里年份用的是fyear
y1, y2 = st.sidebar.slider("Year Range", 
                          int(df['fyear'].min()), 
                          int(df['fyear'].max()), 
                          (int(df['fyear'].min()), int(df['fyear'].max())))

metric = st.sidebar.selectbox("Metric to Display", ["roe", "roa", "pm", "lev"])

# 筛选数据（关键修复：把year改成fyear）
filtered_df = df[
    (df["tic"].isin(companies)) &
    (df["fyear"] >= y1) & (df["fyear"] <= y2)
]

# 显示数据表格
st.subheader("Filtered Financial Data")
st.dataframe(filtered_df[["tic", "conm", "fyear", "sale", "roe", "roa", "pm", "lev"]])

# 绘制图表
st.subheader(f"{metric.upper()} Trend by Company")
fig, ax = plt.subplots(figsize=(10, 6))
for tic in filtered_df["tic"].unique():
    company_data = filtered_df[filtered_df["tic"] == tic].sort_values("fyear")
    ax.plot(company_data["fyear"], company_data[metric], marker='o', label=tic)

ax.set_xlabel("Year")
ax.set_ylabel(metric.upper())
ax.legend()
st.pyplot(fig)
