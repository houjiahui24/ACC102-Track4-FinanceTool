import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

# 读取WRDS数据
df = pd.read_csv("wrds_data.csv")
df["fyear"] = df["fyear"].astype(int)

# 计算四大财务指标（适配你的WRDS字段）
df['roe'] = df['ni'] / df['ceq']
df['roa'] = df['ni'] / df['at']
df['pm'] = df['ni'] / df['sale']
df['lev'] = df['at'] / df['ceq']

# ===================== 侧边栏交互 =====================
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

# ===================== 数据筛选 =====================
df_filtered = df[
    (df["tic"].isin(comps)) &
    (df["fyear"] >= y1) &
    (df["fyear"] <= y2)
]

# Show data table
if show_table:
    st.subheader("Data")
    st.dataframe(df_filtered.round(decimals))

# ---------------------- 1. 折线图 Trend ----------------------
st.subheader(f"Trend: {metric.upper()}")
fig1, ax1 = plt.subplots(figsize=(chart_width, 4))

for company in comps:
    c_data = df_filtered[df_filtered["tic"] == company].sort_values("fyear")
    ax1.plot(c_data["fyear"], c_data[metric], marker='o', label=company)

if show_avg:
    avg_data = df_filtered.groupby("fyear")[metric].mean()
    ax1.plot(avg_data.index, avg_data, 'k--', label='Average', linewidth=2)

ax1.set_xlabel("Year")
ax1.set_ylabel(metric.upper())
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ---------------------- 2. 散点图 Scatter（已修复） ----------------------
st.subheader(f"Scatter Plot: {x_var.upper()} vs {y_var.upper()}")
fig2, ax2 = plt.subplots(figsize=(chart_width, 4))
for company in comps:
    # 修复点：按公司代码筛选数据
    c_data = df_filtered[df_filtered["tic"] == company]
    ax2.scatter(c_data[x_var], c_data[y_var], label=company, s=60)
ax2.set_xlabel(x_var.upper())
ax2.set_ylabel(y_var.upper())
ax2.legend()
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ---------------------- 3. 柱状图 Bar ----------------------
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

# ---------------------- 4. 雷达图 Radar Chart ----------------------
st.subheader("Radar Chart – Financial Performance Comparison")
# 取各公司均值
radar_df = df_filtered.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

# 雷达图指标标签
labels = ['ROE', 'ROA', 'Profit Margin', 'Leverage']
num_vars = len(labels)

# 角度均分
angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]

fig4 = plt.figure(figsize=(7, 7))
ax4 = fig4.add_subplot(111, polar=True)

# 每家公司画一条雷达线
for _, row in radar_df.iterrows():
    values = [row["roe"], row["roa"], row["pm"], row["lev"]]
    values += values[:1]
    ax4.plot(angles, values, marker='o', label=row["tic"])
    ax4.fill(angles, values, alpha=0.1)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
st.pyplot(fig4)
