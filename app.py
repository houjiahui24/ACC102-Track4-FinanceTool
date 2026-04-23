import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

# 读取并处理数据
df = pd.read_csv("wrds_data.csv")
df["fyear"] = df["fyear"].astype(int)

# 计算四大财务指标（适配WRDS字段）
df['roe'] = df['ni'] / df['ceq']
df['roa'] = df['ni'] / df['at']
df['pm'] = df['ni'] / df['sale']
df['lev'] = df['at'] / df['ceq']

# ===================== 侧边栏交互 =====================
st.sidebar.header("Settings")

# 公司选择（默认四家全选）
comps = st.sidebar.multiselect(
    "Companies",
    ["AAPL", "MSFT", "NVDA", "GOOGL"],
    default=["AAPL", "MSFT", "NVDA", "GOOGL"]
)

# 年份范围
y1, y2 = st.sidebar.slider("Year Range", 2020, 2024, (2020, 2024))

# 主指标选择
metric = st.sidebar.selectbox(
    "Metric to Display",
    ["roe", "roa", "pm", "lev"]
)

# 额外选项
show_avg = st.sidebar.checkbox("Show Average Line", False)
decimals = st.sidebar.slider("Decimal Places", 1, 4, 2)
show_table = st.sidebar.checkbox("Show Data Table", True)
chart_width = st.sidebar.slider("Chart Width", 6, 12, 10)

# 散点图XY轴自定义
x_var = st.sidebar.selectbox("Scatter Plot X Variable", ["roe", "roa", "pm", "lev", "sale"])
y_var = st.sidebar.selectbox("Scatter Plot Y Variable", ["roe", "roa", "pm", "lev", "sale"])

# ===================== 数据筛选 =====================
df_filtered = df[
    (df["tic"].isin(comps)) &
    (df["fyear"] >= y1) &
    (df["fyear"] <= y2)
]

# 显示数据表
if show_table:
    st.subheader("Filtered Data Table")
    st.dataframe(df_filtered.round(decimals), use_container_width=True)

# ---------------------- 1. 折线图：四家公司多年份趋势对比 ----------------------
st.subheader(f"1. Line Chart: {metric.upper()} Trend (All Companies & Years)")
fig1, ax1 = plt.subplots(figsize=(chart_width, 4))

for company in comps:
    # 按公司筛选，按年份排序
    c_data = df_filtered[df_filtered["tic"] == company].sort_values("fyear")
    ax1.plot(c_data["fyear"], c_data[metric], marker='o', linewidth=2, label=company)

# 显示均值线
if show_avg:
    avg_data = df_filtered.groupby("fyear")[metric].mean()
    ax1.plot(avg_data.index, avg_data, 'k--', label='Industry Average', linewidth=2)

ax1.set_xlabel("Year")
ax1.set_ylabel(metric.upper())
ax1.legend(title="Company")
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ---------------------- 2. 散点图：四家公司多年份数据点对比 ----------------------
st.subheader(f"2. Scatter Plot: {x_var.upper()} vs {y_var.upper()} (All Companies & Years)")
fig2, ax2 = plt.subplots(figsize=(chart_width, 4))

for company in comps:
    # 按公司筛选（已修复之前的错误）
    c_data = df_filtered[df_filtered["tic"] == company]
    ax2.scatter(c_data[x_var], c_data[y_var], s=80, label=company, alpha=0.7)

ax2.set_xlabel(x_var.upper())
ax2.set_ylabel(y_var.upper())
ax2.legend(title="Company")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ---------------------- 3. 柱状图：四家公司多年份营收对比 ----------------------
st.subheader("3. Bar Chart: Annual Revenue Comparison (All Companies & Years)")
fig3, ax3 = plt.subplots(figsize=(chart_width, 4))

# 透视表：年份为行，公司为列，值为营收
pivot_sale = df_filtered.pivot(index="fyear", columns="tic", values="sale")
pivot_sale.plot(kind="bar", ax=ax3)

ax3.set_xlabel("Year")
ax3.set_ylabel("Revenue")
ax3.legend(title="Company")
ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ---------------------- 4. 雷达图：四家公司多年份平均表现对比 ----------------------
st.subheader("4. Radar Chart: Average Financial Performance (All Companies)")
# 计算每家公司2020-2024的平均指标
radar_df = df_filtered.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

labels = ['ROE', 'ROA', 'Profit Margin', 'Leverage']
num_vars = len(labels)
angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
angles += angles[:1]

fig4 = plt.figure(figsize=(7, 7))
ax4 = fig4.add_subplot(111, polar=True)

for _, row in radar_df.iterrows():
    values = [row["roe"], row["roa"], row["pm"], row["lev"]]
    values += values[:1]
    ax4.plot(angles, values, marker='o', linewidth=2, label=row["tic"])
    ax4.fill(angles, values, alpha=0.15)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1))
st.pyplot(fig4)
