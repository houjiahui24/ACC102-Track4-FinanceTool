import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="ACC102 Financial Dashboard", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data Source: WRDS Compustat | Period: 2020-2024")

@st.cache_data
def load_data():
    df = pd.read_csv("wrds_data.csv")
    df["fyear"] = df["fyear"].astype(int)
    df['roe'] = df['ni'] / df['ceq']
    df['roa'] = df['ni'] / df['at']
    df['pm'] = df['ni'] / df['sale']
    df['lev'] = df['at'] / df['ceq']
    return df

df = load_data()

# ---------------------- Sidebar Enhanced Comparison Interactions ----------------------
st.sidebar.header("Settings & Data Comparison")

# Basic select
all_companies = sorted(df["tic"].unique())
selected_companies = st.sidebar.multiselect(
    "Select Companies",
    options=all_companies,
    default=all_companies
)

min_y = int(df["fyear"].min())
max_y = int(df["fyear"].max())
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=min_y,
    max_value=max_y,
    value=(min_y, max_y)
)

choose_metric = st.sidebar.selectbox(
    "Select Main Analysis Metric",
    options=["roe", "roa", "pm", "lev"]
)

# New 1: Two company direct comparison
st.sidebar.divider()
st.sidebar.subheader("Two Companies Comparison")
comp1 = st.sidebar.selectbox("Company A", all_companies, index=0)
comp2 = st.sidebar.selectbox("Company B", all_companies, index=1)

# New 2: Performance rank filter
st.sidebar.divider()
rank_choice = st.sidebar.radio(
    "Filter by Performance",
    ["All Companies", "Top Performing", "Bottom Performing"]
)

# New 3: Metric value range filter
st.sidebar.divider()
st.sidebar.subheader("Metric Range Filter")
metric_low = st.sidebar.slider("Minimum Metric Value", 0.0, 1.0, 0.0)
metric_high = st.sidebar.slider("Maximum Metric Value", 0.0, 1.0, 1.0)

# Display settings
st.sidebar.divider()
show_grid = st.sidebar.checkbox("Show Grid in Charts", value=True)
fig_size_choice = st.sidebar.radio("Chart Size", ["Small", "Standard", "Large"], index=1)
decimal_digits = st.sidebar.slider("Decimal Places", 1, 4, 3)
show_table = st.sidebar.checkbox("Show Raw Data Table", value=True)
show_stats = st.sidebar.checkbox("Show Statistics Summary", value=True)

# ---------------------- Data Filtering ----------------------
filtered_df = df[
    (df["tic"].isin(selected_companies)) &
    df["fyear"].between(start_year, end_year) &
    (df[choose_metric] >= metric_low) &
    (df[choose_metric] <= metric_high)
]

# Top / Bottom rank filter
if rank_choice == "Top Performing":
    top_tic = filtered_df.groupby("tic")[choose_metric].mean().idxmax()
    filtered_df = filtered_df[filtered_df["tic"] == top_tic]
elif rank_choice == "Bottom Performing":
    bot_tic = filtered_df.groupby("tic")[choose_metric].mean().idxmin()
    filtered_df = filtered_df[filtered_df["tic"] == bot_tic]

size_map = {"Small":(8,4), "Standard":(10,5), "Large":(12,6)}
fig_w, fig_h = size_map[fig_size_choice]

# ---------------------- Comparison Text Panel ----------------------
st.subheader("📊 Average Metric Comparison Panel")
comp_avg = filtered_df.groupby("tic")[["roe","roa","pm","lev"]].mean().round(decimal_digits)
st.dataframe(comp_avg, use_container_width=True)

# Direct two company compare
st.subheader("🤝 Direct Comparison: {} vs {}".format(comp1, comp2))
c1_avg = df[df["tic"]==comp1][choose_metric].mean()
c2_avg = df[df["tic"]==comp2][choose_metric].mean()
st.write(f"{comp1} Average {choose_metric.upper()}: {c1_avg:.{decimal_digits}f}")
st.write(f"{comp2} Average {choose_metric.upper()}: {c2_avg:.{decimal_digits}f}")

# ---------------------- Data Table & Stats ----------------------
if show_table:
    st.subheader("Filtered Raw Data Table")
    st.dataframe(filtered_df.round(decimal_digits), use_container_width=True)

if show_stats:
    st.subheader("Descriptive Statistics Summary")
    st.write(filtered_df[["roe","roa","pm","lev"]].describe().round(decimal_digits))

# ---------------------- 1. Line Chart ----------------------
st.subheader("1. Line Chart – Financial Metric Trend")
fig1, ax1 = plt.subplots(figsize=(fig_w, fig_h))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"] == tic].sort_values("fyear")
    ax1.plot(d["fyear"], d[choose_metric], marker='o', linewidth=2, label=tic)
ax1.set_xlabel("Year")
ax1.set_ylabel(choose_metric.upper())
ax1.legend()
if show_grid:
    ax1.grid(alpha=0.3)
st.pyplot(fig1)

# ---------------------- 2. Bar Chart ----------------------
st.subheader("2. Bar Chart – Annual Revenue Comparison")
fig2, ax2 = plt.subplots(figsize=(fig_w, fig_h))
pivot_sale = filtered_df.pivot(index="fyear", columns="tic", values="sale")
pivot_sale.plot(kind="bar", ax=ax2)
ax2.set_xlabel("Year")
ax2.set_ylabel("Revenue")
ax2.legend(title="Company")
if show_grid:
    ax2.grid(alpha=0.3)
st.pyplot(fig2)

# ---------------------- 3. Scatter Plot ----------------------
st.subheader("3. Scatter Plot – ROA vs Profit Margin")
fig3, ax3 = plt.subplots(figsize=(fig_w, fig_h))
for tic in filtered_df["tic"].unique():
    d = filtered_df[filtered_df["tic"] == tic]
    ax3.scatter(d["roa"], d["pm"], s=80, label=tic)
ax3.set_xlabel("ROA")
ax3.set_ylabel("Profit Margin")
ax3.legend()
if show_grid:
    ax3.grid(alpha=0.3)
st.pyplot(fig3)

# ---------------------- 4. Radar Chart ----------------------
st.subheader("4. Radar Chart – Overall Financial Performance")
mean_df = filtered_df.groupby("tic")[["roe","roa","pm","lev"]].mean().reset_index()

labels = ['ROE','ROA','Profit Margin','Leverage']
angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
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
