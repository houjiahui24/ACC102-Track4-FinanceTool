import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 全局设置
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False
st.set_page_config(page_title="ACC102 Financial Dashboard", layout="wide")

# 标题
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data Source: WRDS Compustat | Period: 2020-2024")

# 加载WRDS数据
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

# 所有公司列表，默认全部选中
all_tics = df["tic"].unique()

# ---------------------- 侧边栏交互 ----------------------
st.sidebar.header("Dashboard Settings")

# 公司选择：默认全选
selected_firms = st.sidebar.multiselect(
    "Select Companies",
    options=all_tics,
    default=all_tics
)

# 年份范围
min_y = int(df["fyear"].min())
max_y = int(df["fyear"].max())
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=min_y,
    max_value=max_y,
    value=(min_y, max_y)
)

# 选择主指标
main_metric = st.sidebar.selectbox(
    "Select Main Metric",
    options=["roe", "roa", "pm", "lev"]
)

# 图表设置
show_grid = st.sidebar.checkbox("Show Grid", value=True)
decimal_places = st.sidebar.slider("Decimal Places", 1, 4, 3)

# ---------------------- 只做正常筛选，不加任何乱过滤 ----------------------
df_filtered = df[
    (df["tic"].isin(selected_firms)) &
    (df["fyear"] >= start_year) &
    (df["fyear"] <= end_year)
]

# ---------------------- 数据表格 & 统计 ----------------------
st.subheader("Filtered Data Table")
st.dataframe(df_filtered.round(decimal_places), use_container_width=True)

st.subheader("Descriptive Statistics")
st.write(df_filtered[["roe","roa","pm","lev"]].describe().round(decimal_places))

# ---------------------- 1. 折线图 四家对比 ----------------------
st.subheader("1. Line Chart – Financial Metric Trend")
fig1, ax1 = plt.subplots(figsize=(10,5))
for firm in selected_firms:
    data = df_filtered[df_filtered["tic"]==firm].sort_values("fyear")
    ax1.plot(data["fyear"], data[main_metric], marker='o', linewidth=2, label=firm)
ax1.set_xlabel("Year")
ax1.set_ylabel(main_metric.upper())
ax1.legend()
if show_grid:
    ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ---------------------- 2. 柱状图 营收对比 四家 ----------------------
st.subheader("2. Bar Chart – Annual Revenue")
fig2, ax2 = plt.subplots(figsize=(10,5))
pivot_rev = df_filtered.pivot(index="fyear", columns="tic", values="sale")
pivot_rev.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Revenue")
ax2.legend(title="Company")
if show_grid:
    ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ---------------------- 3. 散点图 ROA vs PM 四家 ----------------------
st.subheader("3. Scatter Plot – ROA vs Profit Margin")
fig3, ax3 = plt.subplots(figsize=(10,5))
for firm in selected_firms:
    data = df_filtered[df_filtered["tic"]==firm]
    ax3.scatter(data["roa"], data["pm"], s=80, label=firm)
ax3.set_xlabel("ROA")
ax3.set_ylabel("Profit Margin")
ax3.legend()
if show_grid:
    ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ---------------------- 4. 雷达图 四家综合对比 ----------------------
st.subheader("4. Radar Chart – Overall Financial Performance")
radar_df = df_filtered.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

labels = ["ROE","ROA","Profit Margin","Leverage"]
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig4 = plt.figure(figsize=(7,7))
ax4 = fig4.add_subplot(111, polar=True)

for _, row in radar_df.iterrows():
    vals = [row["roe"], row["roa"], row["pm"], row["lev"]]
    vals += vals[:1]
    ax4.plot(angles, vals, marker='o', label=row["tic"])
    ax4.fill(angles, vals, alpha=0.1)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right", bbox_to_anchor=(1.2,1.1))
st.pyplot(fig4)
