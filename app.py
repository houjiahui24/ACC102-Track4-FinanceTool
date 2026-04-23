import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

# 页面设置
st.set_page_config(page_title="ACC102 High Score Dashboard", layout="wide")
st.title("🏆 ACC102 Track4: Financial Performance Dashboard")
st.caption("Data Source: WRDS Compustat (Real Data) | Companies: AAPL, MSFT, NVDA, GOOGL | 2020-2024")

# 读取数据
df = pd.read_csv("wrds_data.csv")

# 侧边栏
st.sidebar.header("Control Panel")
companies = st.sidebar.multiselect(
    "Select Companies",
    ["AAPL", "MSFT", "NVDA", "GOOGL"],
    default=["AAPL", "MSFT", "NVDA", "GOOGL"]
)

year_min, year_max = st.sidebar.slider("Year Range", 2020, 2024, (2020, 2024))
df = df[(df["tic"].isin(companies)) & (df["year"] >= year_min) & (df["year"] <= year_max)]

# 数据预览
st.subheader("📋 Data Preview")
st.dataframe(df.round(3))

# ---------------------- 图1 ROE 趋势 ----------------------
st.subheader("1. ROE Trend")
fig1, ax1 = plt.subplots(figsize=(9, 3.5))
for tic in companies:
    sub = df[df["tic"] == tic]
    ax1.plot(sub["year"], sub["roe"], marker="o", label=tic)
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# ---------------------- 图2 营收柱状图 ----------------------
st.subheader("2. Annual Revenue Comparison")
rev_pivot = df.pivot(index="year", columns="tic", values="sale")
st.bar_chart(rev_pivot)

# ---------------------- 图3 净利率 ----------------------
st.subheader("3. Net Profit Margin Trend")
fig3, ax3 = plt.subplots(figsize=(9, 3.5))
for tic in companies:
    sub = df[df["tic"] == tic]
    ax3.plot(sub["year"], sub["pm"], marker="s", label=tic)
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

# ---------------------- 图4 杠杆率 ----------------------
st.subheader("4. Leverage Level Trend")
lev_pivot = df.pivot(index="year", columns="tic", values="lev")
st.area_chart(lev_pivot)

# ---------------------- 图5 雷达图 ----------------------
st.subheader("5. Financial Radar Chart (Latest Year)")
latest = df[df["year"] == df["year"].max()].copy()
indicators = ["roe", "roa", "pm", "lev"]

def radar(df_sub):
    angles = [i / len(indicators) * 2 * pi for i in range(len(indicators))]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    
    for _, row in df_sub.iterrows():
        values = row[indicators].tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=row["tic"])
        ax.fill(angles, values, alpha=0.15)
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(["ROE", "ROA", "Profit Margin", "Leverage"])
    ax.legend(loc="upper right")
    return fig

if not latest.empty:
    st.pyplot(radar(latest))
else:
    st.info("Please select a valid year to show radar chart")

st.success("✅ All data from WRDS Compustat | Runs locally without password")
