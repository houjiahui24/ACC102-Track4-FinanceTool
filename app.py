import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- 标题 ----------------------
st.title("🏦 ACC102 Interactive Financial Ratio Analyzer")
st.subheader("Gree | Midea | Haier (2018–2024)")

# ---------------------- 完整版财务数据 ----------------------
data = {
    "Year": [2018,2019,2020,2021,2022,2023,2024],
    # ROE
    "Gree_ROE": [22.5,22.2,19.1,21.2,22.6,22.7,22.9],
    "Midea_ROE": [23.4,23.5,22.1,21.5,21.1,20.9,20.6],
    "Haier_ROE": [17.7,17.0,16.6,16.3,15.6,15.8,16.0],
    # Profit Margin (%)
    "Gree_PM": [13.3,12.5,13.0,12.2,12.0,13.6,17.1],
    "Midea_PM": [10.1,9.8,9.5,9.2,8.9,8.7,8.4],
    "Haier_PM": [5.3,6.1,5.4,5.8,6.1,6.4,6.2],
    # Asset Turnover (%)
    "Gree_TO": [78.9,70.0,82.2,83.5,83.1,85.2,85.0],
    "Midea_TO": [98.5,92.1,78.9,88.0,81.4,76.5,67.4],
    "Haier_TO": [110.0,107.1,103.1,104.6,103.3,103.2,98.6],
    # Leverage
    "Gree_LEV": [2.71,2.53,2.39,2.96,3.48,3.05,2.60],
    "Midea_LEV": [3.02,2.88,2.99,2.68,2.49,2.39,2.45],
    "Haier_LEV": [2.85,2.81,2.90,2.88,2.78,2.79,2.65]
}
df = pd.DataFrame(data)

# ---------------------- 交互部分开始 ----------------------
st.sidebar.header("🔧 Control Panel")

# 1. 公司选择框
selected_companies = st.sidebar.multiselect(
    "Select Companies to View",
    ["Gree", "Midea", "Haier"],
    default=["Gree", "Midea", "Haier"]
)

# 2. 指标选择框
selected_ratio = st.sidebar.selectbox(
    "Select Financial Ratio",
    ["ROE (Return on Equity)", "Profit Margin", "Asset Turnover", "Leverage"]
)

# 3. 年份滑块
selected_years = st.slider(
    "Select Year Range",
    min_value=2018, max_value=2024, value=(2018, 2024)
)

# ---------------------- 数据过滤 ----------------------
# 映射指标名称到列名
ratio_mapping = {
    "ROE (Return on Equity)": ["Gree_ROE", "Midea_ROE", "Haier_ROE"],
    "Profit Margin": ["Gree_PM", "Midea_PM", "Haier_PM"],
    "Asset Turnover": ["Gree_TO", "Midea_TO", "Haier_TO"],
    "Leverage": ["Gree_LEV", "Midea_LEV", "Haier_LEV"]
}
cols = ratio_mapping[selected_ratio]

# 过滤年份
mask = (df['Year'] >= selected_years[0]) & (df['Year'] <= selected_years[1])
filtered_df = df[mask]

# ---------------------- 展示内容 ----------------------
st.subheader("📊 Full Financial Data Table")
st.dataframe(filtered_df)

st.subheader(f"📈 {selected_ratio} Trend")
fig, ax = plt.subplots(figsize=(10, 6))

# 循环画选中公司的图
company_names = {"Gree": "Gree_ROE", "Midea": "Midea_ROE", "Haier": "Haier_ROE"}
for company in selected_companies:
    # 根据选中的公司获取对应列
    col_map = {"Gree": "ROE", "Midea": "ROE", "Haier": "ROE"} # 临时映射，实际用上面的cols
    # 修正：直接从选中的cols里匹配公司
    if company == "Gree":
        data_col = cols[0] if "ROE" in cols[0] else cols[3] if "PM" in cols[0] else cols[6] if "TO" in cols[0] else cols[9]
    elif company == "Midea":
        data_col = cols[1] if "ROE" in cols[1] else cols[4] if "PM" in cols[1] else cols[7] if "TO" in cols[1] else cols[10]
    else:
        data_col = cols[2] if "ROE" in cols[2] else cols[5] if "PM" in cols[2] else cols[8] if "TO" in cols[2] else cols[11]
        
    ax.plot(filtered_df['Year'], filtered_df[data_col], marker='o', label=company)

ax.set_title(f"{selected_ratio} Comparison ({selected_years[0]}-{selected_years[1]})")
ax.set_xlabel("Year")
ax.set_ylabel(selected_ratio)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------------------- 结论 ----------------------
st.subheader("💡 Key Insights")
st.markdown("""
- **Midea**: Strongest overall ROE, though slightly declining. Highest asset efficiency.
- **Gree**: Most stable profit margin with significant improvement in 2024. Lowest asset turnover.
- **Haier**: Steady performance at lower profitability levels, but highest asset turnover.
""")
