import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 页面基础设置
st.set_page_config(page_title="ACC102 Financial Dashboard", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat (2020-2024)")

# 读取并处理数据（完全适配WRDS列名）
@st.cache_data
def load_data():
    df = pd.read_csv("wrds_data.csv")
    # 确保年份是整数类型
    df['fyear'] = df['fyear'].astype(int)
    # 计算核心财务指标
    df['roe'] = df['ni'] / df['ceq']  # 净资产收益率
    df['roa'] = df['ni'] / df['at']   # 资产收益率
    df['pm'] = df['ni'] / df['sale']  # 净利率
    df['lev'] = df['at'] / df['ceq']  # 杠杆率
    return df

df = load_data()

# --------------------------
# 侧边栏交互控件（完全适配数据）
# --------------------------
st.sidebar.header("Settings")

# 1. 公司多选（从数据里的tic列自动获取）
companies = st.sidebar.multiselect(
    "Select Companies",
    options=df["tic"].unique(),
    default=df["tic"].unique()
)

# 2. 年份范围滑块（用fyear列，不是year！）
min_year = int(df['fyear'].min())
max_year = int(df['fyear'].max())
y1, y2 = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)

# 3. 指标选择
metric = st.sidebar.selectbox(
    "Select Metric to Display",
    ["roe", "roa", "pm", "lev"]
)

# --------------------------
# 数据筛选（关键修复：全部用fyear）
# --------------------------
filtered_df = df[
    (df["tic"].isin(companies)) &
    df["fyear"].between(y1, y2)
]

# --------------------------
# 主页面展示
# --------------------------
# 1. 数据表格
st.subheader("Filtered Financial Data")
st.dataframe(
    filtered_df[["tic", "conm", "fyear", "sale", "roe", "roa", "pm", "lev"]],
    use_container_width=True
)

# 2. 趋势图
st.subheader(f"{metric.upper()} Trend Comparison")
fig, ax = plt.subplots(figsize=(10, 5))

for tic in filtered_df["tic"].unique():
    # 按公司分组，按年份排序
    company_data = filtered_df[filtered_df["tic"] == tic].sort_values("fyear")
    ax.plot(
        company_data["fyear"], 
        company_data[metric], 
        marker='o', 
        linewidth=2, 
        label=tic
    )

ax.set_xlabel("Year", fontsize=12)
ax.set_ylabel(metric.upper(), fontsize=12)
ax.legend(title="Company")
ax.grid(alpha=0.3)
st.pyplot(fig)
