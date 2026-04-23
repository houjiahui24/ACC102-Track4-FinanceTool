import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# 设置页面
st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat (2020-2024)")

# 读取数据
df = pd.read_csv("wrds_data.csv")

# 侧边栏筛选
st.sidebar.header("Filters")
companies = st.sidebar.multiselect(
    "Select Companies",
    ["AAPL", "MSFT", "NVDA", "GOOGL"],
    default=["AAPL", "MSFT", "NVDA", "GOOGL"]
)
year_start, year_end = st.sidebar.slider("Year Range", 2020, 2024, (2020, 2024))

# 筛选数据
df_filtered = df[(df["tic"].isin(companies)) & (df["year"] >= year_start) & (df["year"] <= year_end)]

# 数据预览
st.subheader("Data Preview")
st.dataframe(df_filtered.round(3))

# 1. ROE 趋势图
st.subheader("1. ROE Trend")
fig1, ax1 = plt.subplots(figsize=(9, 3.5))
for company in companies:
    data = df_filtered[df_filtered["tic"] == company]
    ax1.plot(data["year"], data["roe"], marker="o", label=company)
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# 2. 营收柱状图
st.subheader("2. Annual Revenue")
rev = df_filtered.pivot(index="year", columns="tic", values="sale")
st.bar_chart(rev)

# 3. 净利率趋势
st.subheader("3. Profit Margin Trend")
fig3, ax3 = plt.subplots(figsize=(9, 3.5))
for company in companies:
    data = df_filtered[df_filtered["tic"] == company]
    ax3.plot(data["year"], data["pm"], marker="s", label=company)
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

# 4. 杠杆率面积图
st.subheader("4. Leverage Level")
lev = df_filtered.pivot(index="year", columns="tic", values="lev")
st.area_chart(lev)

# 5. 雷达图
st.subheader("5. Financial Radar Chart (Latest Year)")
latest_year = df_filtered["year"].max()
latest_data = df_filtered[df_filtered["year"] == latest_year].copy()
indicators = ["roe", "roa", "pm", "lev"]

def make_radar(data):
    angles = [i / len(indicators) * 2 * pi for i in range(len(indicators))]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    for _, row in data.iterrows():
        values = row[indicators].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=row["tic"])
        ax.fill(angles, values, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(["ROE", "ROA", "Profit Margin", "Leverage"])
    ax.legend(loc="upper right")
    return fig

if not latest_data.empty:
    st.pyplot(make_radar(latest_data))
else:
    st.info("Please select a valid year range.")
