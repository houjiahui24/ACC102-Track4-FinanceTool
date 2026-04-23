import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

df = pd.read_csv("wrds_data.csv")

# 🔥 修复 1：把年份转成整数，避免出错
df["fyear"] = df["fyear"].astype(int)

# 🔥 修复 2：计算你要用的 4 个指标
df['roe'] = df['ni'] / df['ceq']
df['roa'] = df['ni'] / df['at']
df['pm'] = df['ni'] / df['sale']
df['lev'] = df['at'] / df['ceq']

# ===================== 你原版的所有交互 100% 保留 =====================
st.sidebar.header("Settings")

comps = st.sidebar.multiselect(
    "Companies",
    ["AAPL", "MSFT", "NVDA", "GOOGL"],
    default=["AAPL", "MSFT", "NVDA", "GOOGL"]
)

y1, y2 = st.sidebar.slider("Year Range", 2020, 2024, (2020, 2024))

metric = st.sidebar.selectbox(
    "Metric to Display",
    ["roe", "roa", "pm", "lev"]
)

show_growth = st.sidebar.checkbox("Show Revenue Growth", False)
show_avg = st.sidebar.checkbox("Show Average Line", False)

decimals = st.sidebar.slider("Decimal Places", 1, 4, 2)
show_table = st.sidebar.checkbox("Show Data Table", True)
chart_width = st.sidebar.slider("Chart Width", 6, 12, 8)

# Relationship analysis: scatter plot variables
x_var = st.sidebar.selectbox("X Variable", ["roe", "roa", "pm", "lev", "sale"])
y_var = st.sidebar.selectbox("Y Variable", ["roe", "roa", "pm", "lev", "sale"])

# Single year comparison
selected_year = st.sidebar.selectbox("Single Year Comparison", [2020,2021,2022,2023,2024])

# ===================== 🔥 核心修复：把 year 改成 fyear =====================
df_filtered = df[
    (df["tic"].isin(comps)) &
    (df["fyear"] >= y1) &
    (df["fyear"] <= y2)
]

# Show data table
if show_table:
    st.subheader("Data")
    st.dataframe(df_filtered.round(decimals))

# Main trend chart
st.subheader(f"Trend: {metric.upper()}")
fig1, ax1 = plt.subplots(figsize=(chart_width, 4))

# 绘制折线图（四家公司都显示）
for company in comps:
    c_data = df_filtered[df_filtered["tic"] == company].sort_values("fyear")
    ax1.plot(c_data["fyear"], c_data[metric], marker='o', label=company)

# 显示均值线
if show_avg:
    avg_data = df_filtered.groupby("fyear")[metric].mean()
    ax1.plot(avg_data.index, avg_data, 'k--', label='Average', linewidth=2)

ax1.set_xlabel("Year")
ax1.set_ylabel(metric.upper())
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# 你要的散点图
st.subheader(f"Scatter: {x_var.upper()} vs {y_var.upper()}")
fig2, ax2 = plt.subplots(figsize=(chart_width, 4))
for company in comps:
    c_data = df_filtered[df_filtered["tic"] == company]
    ax2.scatter(c_data[x_var], c_data[y_var], label=company, s=60)
ax2.set_xlabel(x_var.upper())
ax2.set_ylabel(y_var.upper())
ax2.legend()
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# 单年份柱状对比
st.subheader(f"Bar Comparison in {selected_year}")
year_data = df_filtered[df_filtered["fyear"] == selected_year]
if not year_data.empty:
    fig3, ax3 = plt.subplots(figsize=(chart_width, 4))
    ax3.bar(year_data["tic"], year_data[metric])
    ax3.set_ylabel(metric.upper())
    ax3.grid(alpha=0.3)
    st.pyplot(fig3)
else:
    st.info("No data for selected year.")
