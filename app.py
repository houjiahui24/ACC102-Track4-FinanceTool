import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="ACC102 Dashboard", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

@st.cache_data
def load_data():
    df = pd.read_csv("wrds_data.csv")
    df["fyear"] = df["fyear"].astype(int)
    # 计算四个财务指标
    df['roe'] = df['ni'] / df['ceq']
    df['roa'] = df['ni'] / df['at']
    df['pm'] = df['ni'] / df['sale']
    df['lev'] = df['at'] / df['ceq']
    return df

df = load_data()

# 侧边栏筛选
st.sidebar.header("Settings")
companies = st.sidebar.multiselect(
    "Select Companies",
    df["tic"].unique(),
    default=df["tic"].unique()
)

min_year = int(df["fyear"].min())
max_year = int(df["fyear"].max())
y1, y2 = st.sidebar.slider("Select Year Range", min_year, max_year, (min_year, max_year))

# 数据筛选（只用fyear，杜绝报错）
filtered_df = df[
    (df["tic"].isin(companies)) &
    df["fyear"].between(y1, y2)
]

# 显示数据表
st.subheader("Filtered Financial Data")
st.dataframe(filtered_df[["tic","conm","fyear","sale","roe","roa","pm","lev"]], use_container_width=True)

# ====================== 1. 折线图 ROE 趋势 ======================
st.subheader("1. Line Chart — ROE Trend")
fig1, ax1 = plt.subplots(figsize=(10,5))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"]==tic].sort_values("fyear")
    ax1.plot(d["fyear"], d["roe"], marker='o', linewidth=2, label=tic)
ax1.set_xlabel("Year")
ax1.set_ylabel("ROE")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ====================== 2. 柱状图 营业收入 ======================
st.subheader("2. Bar Chart — Revenue")
fig2, ax2 = plt.subplots(figsize=(10,5))
pivot_sale = filtered_df.pivot(index="fyear", columns="tic", values="sale")
pivot_sale.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Revenue")
ax2.legend(title="Company")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ====================== 3. 散点图 ROA vs 净利率 ======================
st.subheader("3. Scatter Plot — ROA vs Profit Margin")
fig3, ax3 = plt.subplots(figsize=(10,5))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"]==tic]
    ax3.scatter(d["roa"], d["pm"], s=80, label=tic)
ax3.set_xlabel("ROA")
ax3.set_ylabel("Profit Margin")
ax3.legend()
ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ====================== 4. 雷达图 财务指标对比 ======================
st.subheader("4. Radar Chart — Financial Indicators")
# 取每家公司均值做雷达图
mean_df = filtered_df.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

labels = ['ROE','ROA','Profit Margin','Leverage']
angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
angles += angles[:1]

fig4 = plt.figure(figsize=(6,6))
ax4 = fig4.add_subplot(111, polar=True)

for _, row in mean_df.iterrows():
    values = [row["roe"], row["roa"], row["pm"], row["lev"]]
    values += values[:1]
    ax4.plot(angles, values, marker='o', label=row["tic"])
    ax4.fill(angles, values, alpha=0.1)

ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right", bbox_to_anchor=(1.2,1.1))
st.pyplot(fig4)
