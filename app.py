import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 全局字体设置
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="ACC102 Financial Dashboard", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("wrds_data.csv")
    df["fyear"] = df["fyear"].astype(int)
    # 计算四大财务指标
    df['roe'] = df['ni'] / df['ceq']
    df['roa'] = df['ni'] / df['at']
    df['pm'] = df['ni'] / df['sale']
    df['lev'] = df['at'] / df['ceq']
    return df

df = load_data()

# ===================== 侧边栏 超多交互控件 =====================
st.sidebar.header("🔧 数据交互设置")

# 1. 选择公司
selected_companies = st.sidebar.multiselect(
    "选择对比公司",
    options=df["tic"].unique(),
    default=df["tic"].unique()
)

# 2. 年份范围选择
min_y = int(df["fyear"].min())
max_y = int(df["fyear"].max())
start_year, end_year = st.sidebar.slider(
    "选择年份范围",
    min_value=min_y,
    max_value=max_y,
    value=(min_y, max_y)
)

# 3. 单独选择要分析的财务指标
choose_metric = st.sidebar.selectbox(
    "选择主分析指标",
    options=["roe","roa","pm","lev"],
    index=0
)

# 4. 图表风格设置
show_grid = st.sidebar.checkbox("显示图表网格", value=True)
fig_size_choice = st.sidebar.radio("图表尺寸", ["偏小","标准","偏大"], index=1)

# 5. 筛选ROE最小值，过滤异常值
roe_min = st.sidebar.slider("ROE 最低筛选值", 0.0, 1.0, 0.0)

# ===================== 数据筛选 =====================
filtered_df = df[
    (df["tic"].isin(selected_companies)) &
    df["fyear"].between(start_year, end_year) &
    (df["roe"] >= roe_min)
]

# 映射图表尺寸
size_map = {"偏小":(8,4), "标准":(10,5), "偏大":(12,6)}
fig_w, fig_h = size_map[fig_size_choice]

# ===================== 页面：基础数据展示 =====================
st.subheader("📋 筛选后原始数据")
st.dataframe(filtered_df[["tic","conm","fyear","sale","roe","roa","pm","lev"]], use_container_width=True)

# 数据统计摘要
st.subheader("📊 数据统计摘要")
st.write(filtered_df[["roe","roa","pm","lev"]].describe().round(3))

# ===================== 1. 折线图（选定指标年度趋势） =====================
st.subheader("1. 折线图 — 财务指标年度趋势")
fig1, ax1 = plt.subplots(figsize=(fig_w, fig_h))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"]==tic].sort_values("fyear")
    ax1.plot(d["fyear"], d[choose_metric], marker='o', linewidth=2, label=tic)
ax1.set_xlabel("Year")
ax1.set_ylabel(choose_metric.upper())
ax1.legend()
if show_grid:
    ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ===================== 2. 柱状图 — 营业收入对比 =====================
st.subheader("2. 柱状图 — 各公司年度营收")
fig2, ax2 = plt.subplots(figsize=(fig_w, fig_h))
pivot_sale = filtered_df.pivot(index="fyear", columns="tic", values="sale")
pivot_sale.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Revenue")
ax2.legend(title="Company")
if show_grid:
    ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ===================== 3. 散点图 — ROA 与 净利率 相关性 =====================
st.subheader("3. 散点图 — ROA vs 净利率 相关性")
fig3, ax3 = plt.subplots(figsize=(fig_w, fig_h))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"]==tic]
    ax3.scatter(d["roa"], d["pm"], s=80, label=tic)
ax3.set_xlabel("ROA")
ax3.set_ylabel("Profit Margin")
ax3.legend()
if show_grid:
    ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ===================== 4. 雷达图 — 四项财务指标综合对比 =====================
st.subheader("4. 雷达图 — 多公司财务指标综合对比")
mean_df = filtered_df.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

labels = ['ROE','ROA','Profit Margin','Leverage']
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig4 = plt.figure(figsize=(7,7))
ax4 = fig4.add_subplot(111, polar=True)

for _, row in mean_df.iterrows():
    values = [row["roe"], row["roa"], row["pm"], row["lev"]]
    values += values[:1]
    ax4.plot(angles, values, marker='o', label=row["tic"])
    ax4.fill(angles, values, alpha=0.1)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right", bbox_to_anchor=(1.25,1.1))
st.pyplot(fig4)
