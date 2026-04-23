import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat 2020-2024")

df = pd.read_csv("wrds_data.csv")

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

# Filter data
df_filtered = df[
    (df["tic"].isin(comps)) &
    (df["year"] >= y1) &
    (df["year"] <= y2)
]

# Show data table
if show_table:
    st.subheader("Data")
    st.dataframe(df_filtered.round(decimals))

# Main trend chart
st.subheader(f"Trend: {metric.upper()}")
fig1, ax1 = plt.subplots(figsize=(chart_width, 4))

for c in comps:
    data = df_filtered[df_filtered["tic"] == c]
    ax1.plot(data["year"], data[metric], marker="o", label=c)

if show_avg:
    avg_val = df_filtered.groupby("year")[metric].mean()
    ax1.plot(avg_val.index, avg_val, "k--", label="Average")

ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# Revenue
st.subheader("Revenue")
rev = df_filtered.pivot(index="year", columns="tic", values="sale")
st.bar_chart(rev)

# Growth rate
if show_growth:
    st.subheader("Revenue Growth Rate")
    growth = df_filtered.copy()
    growth["growth"] = growth.groupby("tic")["sale"].pct_change() * 100
    growth_pivot = growth.pivot(index="year", columns="tic", values="growth")
    st.line_chart(growth_pivot.dropna())

# Profit margin
st.subheader("Profit Margin")
fig3, ax3 = plt.subplots(figsize=(chart_width, 4))
for c in comps:
    data = df_filtered[df_filtered["tic"] == c]
    ax3.plot(data["year"], data["pm"], marker="s", label=c)
ax3.legend()
ax3.grid(True)
st.pyplot(fig3)

# Leverage
st.subheader("Leverage")
lev = df_filtered.pivot(index="year", columns="tic", values="lev")
st.area_chart(lev)

# Scatter plot (relationship between two variables)
st.subheader(f"Scatter: {x_var} vs {y_var}")
fig4, ax4 = plt.subplots(figsize=(chart_width, 4))
for c in comps:
    data = df_filtered[df_filtered["tic"] == c]
    ax4.scatter(data[x_var], data[y_var], label=c)
ax4.set_xlabel(x_var)
ax4.set_ylabel(y_var)
ax4.legend()
ax4.grid(True)
st.pyplot(fig4)

# Single year comparison
st.subheader(f"Comparison in {selected_year}")
year_data = df_filtered[df_filtered["year"] == selected_year]
if not year_data.empty:
    st.dataframe(year_data.round(decimals))
else:
    st.write("No data for selected year.")

# Radar chart
st.subheader("Radar Chart (Latest Year)")
latest = df_filtered["year"].max()
latest_data = df_filtered[df_filtered["year"] == latest]

indicators = ["roe", "roa", "pm", "lev"]

def make_radar(data):
    angles = [i / len(indicators) * 2 * np.pi for i in range(len(indicators))]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={"polar": True})
    for _, row in data.iterrows():
        values = row[indicators].tolist()
        values += values[:1]
        ax.plot(angles, values, label=row["tic"])
        ax.fill(angles, values, alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(["ROE", "ROA", "Profit Margin", "Leverage"])
    ax.legend()
    return fig

st.pyplot(make_radar(latest_data))
