import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------- 页面标题 ----------------------
st.title("🏦 ACC102 Interactive Financial Ratio Analyzer")
st.subheader("Gree | Midea | Haier (2018–2024)")

# ---------------------- 数据定义 ----------------------
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

# ---------------------- 交互控制面板 ----------------------
st.sidebar.header("🔧 Control Panel")

# 1. 选择公司
selected_companies = st.sidebar.multiselect(
    "Select Companies to View",
    ["Gree", "Midea", "Haier"],
    default=["Gree", "Midea", "Haier"]
)

# 2. 选择财务指标
selected_ratio = st.sidebar.selectbox(
    "Select Financial Ratio",
    ["ROE (Return on Equity)", "Profit Margin", "Asset Turnover", "Leverage"]
)

# 3. 选择年份范围
year_min, year_max = st.sidebar.slider(
    "Select Year Range",
    min_value=2018, max_value=2024, value=(2018, 2024)
)

# ---------------------- 数据映射与过滤 ----------------------
# 指标和对应列的映射
ratio_map = {
    "ROE (Return on Equity)": {"Gree": "Gree_ROE", "Midea": "Midea_ROE", "Haier": "Haier_ROE"},
    "Profit Margin": {"Gree": "Gree_PM", "Midea": "Midea_PM", "Haier": "Haier_PM"},
    "Asset Turnover": {"Gree": "Gree_TO", "Midea": "Midea_TO", "Haier": "Haier_TO"},
    "Leverage": {"Gree": "Gree_LEV", "Midea": "Midea_LEV", "Haier": "Haier_LEV"}
}
# 过滤年份
filtered_df = df[(df["Year"] >= year_min) & (df["Year"] <= year_max)]

# ---------------------- 展示数据表格 ----------------------
st.subheader("📊 Full Financial Data Table")
st.dataframe(filtered_df)

# ---------------------- 画趋势图 ----------------------
st.subheader(f"📈 {selected_ratio} Trend")
fig, ax = plt.subplots(figsize=(10, 6))

# 根据选中的公司和指标画图
for company in selected_companies:
    col = ratio_map[selected_ratio][company]
    ax.plot(filtered_df["Year"], filtered_df[col], marker='o', label=company)

ax.set_title(f"{selected_ratio} Comparison ({year_min}-{year_max})")
ax.set_xlabel("Year")
ax.set_ylabel(selected_ratio)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# ---------------------- 关键结论 ----------------------
st.subheader("💡 Key Insights")
st.markdown("""
- **Midea**: Strongest overall ROE, though slightly declining. Highest asset efficiency.
- **Gree**: Most stable profit margin with significant improvement in 2024.
- **Haier**: Steady performance at lower profitability levels, but highest asset turnover.
""")
