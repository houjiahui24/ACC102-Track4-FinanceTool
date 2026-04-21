import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ====================== 标题 ======================
st.title("🏦 ACC102 Interactive Financial Analysis Tool")
st.subheader("Gree | Midea | Haier 2018–2024")
st.caption("Data Source: Yahoo Finance & WRDS | Accessed: 21 April 2026")

# ====================== 财务数据 ======================
data = {
    "Year": [2018,2019,2020,2021,2022,2023,2024],
    "Gree_ROE": [22.5,22.2,19.1,21.2,22.6,22.7,22.9],
    "Midea_ROE": [23.4,23.5,22.1,21.5,21.1,20.9,20.6],
    "Haier_ROE": [17.7,17.0,16.6,16.3,15.6,15.8,16.0],
    "Gree_PM": [13.3,12.5,13.0,12.2,12.0,13.6,17.1],
    "Midea_PM": [10.1,9.8,9.5,9.2,8.9,8.7,8.4],
    "Haier_PM": [5.3,6.1,5.4,5.8,6.1,6.4,6.2],
    "Gree_TO": [78.9,70.0,82.2,83.5,83.1,85.2,85.0],
    "Midea_TO": [98.5,92.1,78.9,88.0,81.4,76.5,67.4],
    "Haier_TO": [110.0,107.1,103.1,104.6,103.3,103.2,98.6],
    "Gree_LEV": [2.71,2.53,2.39,2.96,3.48,3.05,2.60],
    "Midea_LEV": [3.02,2.88,2.99,2.68,2.49,2.39,2.45],
    "Haier_LEV": [2.85,2.81,2.90,2.88,2.78,2.79,2.65]
}
df = pd.DataFrame(data)

# ====================== 交互控制面板 ======================
st.sidebar.header("🔧 Interactive Control Panel")

# 选择公司
companies = st.sidebar.multiselect(
    "Choose Companies",
    ["Gree","Midea","Haier"],
    default=["Gree","Midea","Haier"]
)

# 选择指标
indicator = st.sidebar.selectbox(
    "Choose Financial Indicator",
    ["ROE","Profit Margin","Asset Turnover","Leverage"]
)

# 选择年份
year_range = st.sidebar.slider(
    "Year Range",
    2018,2024,(2018,2024)
)

# 过滤数据
start_year, end_year = year_range
df_filter = df[(df.Year >= start_year) & (df.Year <= end_year)]

# 指标映射
col_map = {
    "ROE": {"Gree":"Gree_ROE","Midea":"Midea_ROE","Haier":"Haier_ROE"},
    "Profit Margin": {"Gree":"Gree_PM","Midea":"Midea_PM","Haier":"Haier_PM"},
    "Asset Turnover": {"Gree":"Gree_TO","Midea":"Midea_TO","Haier":"Haier_TO"},
    "Leverage": {"Gree":"Gree_LEV","Midea":"Midea_LEV","Haier":"Haier_LEV"}
}

# ====================== 图1：数据总表 ======================
st.subheader("📋 Full Financial Data")
st.dataframe(df_filter, use_container_width=True)

# ====================== 图2：趋势图 ======================
st.subheader(f"📈 {indicator} Trend Comparison")
fig1, ax1 = plt.subplots(figsize=(10,5))
for c in companies:
    ax1.plot(df_filter.Year, df_filter[col_map[indicator][c]], marker='o', linewidth=2, label=c)
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ====================== 图3：杜邦分析（单公司） ======================
if len(companies) == 1:
    c = companies[0]
    st.subheader(f"🔍 DuPont Analysis — {c}")
    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(df_filter.Year, df_filter[f"{c}_PM"], marker='s', label="Profit Margin")
    ax2.plot(df_filter.Year, df_filter[f"{c}_TO"], marker='^', label="Asset Turnover")
    ax2.plot(df_filter.Year, df_filter[f"{c}_LEV"], marker='*', label="Leverage")
    ax2.legend()
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)

# ====================== 图4：2024柱状对比 ======================
st.subheader("📊 2024 Key Indicators Bar Chart")
df2024 = df[df.Year == 2024].iloc[0]
names = ["Gree","Midea","Haier"]
roe   = [df2024.Gree_ROE, df2024.Midea_ROE, df2024.Haier_ROE]
pm    = [df2024.Gree_PM, df2024.Midea_PM, df2024.Haier_PM]
to    = [df2024.Gree_TO, df2024.Midea_TO, df2024.Haier_TO]
lev   = [df2024.Gree_LEV, df2024.Midea_LEV, df2024.Haier_LEV]

fig3, ((ax3a, ax3b), (ax3c, ax3d)) = plt.subplots(2,2,figsize=(12,8))
ax3a.bar(names, roe, color=['blue','orange','green']); ax3a.set_title("ROE")
ax3b.bar(names, pm, color=['blue','orange','green']); ax3b.set_title("Profit Margin")
ax3c.bar(names, to, color=['blue','orange','green']); ax3c.set_title("Asset Turnover")
ax3d.bar(names, lev, color=['blue','orange','green']); ax3d.set_title("Leverage")
st.pyplot(fig3)

# ====================== 图5：雷达图 ======================
st.subheader("🎯 2024 Financial Ability Radar Chart")
fig4 = plt.figure(figsize=(6,6))
ax4 = fig4.add_subplot(111, polar=True)
labels = ["ROE","Profit Margin","Asset Turnover","Leverage"]
angles = np.linspace(0, 2*np.pi, 4, endpoint=False).tolist()
angles += angles[:1]

for c in companies:
    vals = [
        df2024[col_map["ROE"][c]] / 25,
        df2024[col_map["Profit Margin"][c]] / 20,
        df2024[col_map["Asset Turnover"][c]] / 120,
        df2024[col_map["Leverage"][c]] / 4
    ]
    vals += vals[:1]
    ax4.plot(angles, vals, linewidth=2, label=c)
    ax4.fill(angles, vals, alpha=0.1)
ax4.set_xticks(angles[:-1])
ax4.set_xticklabels(labels)
ax4.legend(loc="upper right")
st.pyplot(fig4)

# ====================== 结论 ======================
st.subheader("💡 Key Insights")
st.markdown("""
- **Midea**: Highest ROE overall, but shows a slight long-term decline.
- **Gree**: Strongest profit margin and improved significantly in 2024.
- **Haier**: Highest asset turnover but relatively lower profitability.
- All three companies maintain stable and safe leverage levels.
""")
