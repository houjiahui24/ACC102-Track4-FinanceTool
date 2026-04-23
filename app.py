import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import pi

st.set_page_config(page_title="ACC102 Project", layout="wide")
st.title("ACC102 Financial Analysis Dashboard")
st.caption("Data from WRDS Compustat (2020-2024)")

df = pd.read_csv("wrds_data.csv")

st.sidebar.header("Filters")

companies = st.sidebar.multiselect(
    "Choose Companies",
    ["AAPL", "MSFT", "NVDA", "GOOGL"],
    default=["AAPL", "MSFT", "NVDA", "GOOGL"]
)

year_start, year_end = st.sidebar.slider(
    "Year Range",
    2020, 2024, (2020, 2024)
)

show_roe = st.sidebar.checkbox("Show ROE Chart", value=True)
show_profit = st.sidebar.checkbox("Show Profit Margin Chart", value=True)
show_leverage = st.sidebar.checkbox("Show Leverage Chart", value=True)

chart_width = st.sidebar.slider("Chart Width", 5, 10, 8)

df_filtered = df[
    (df["tic"].isin(companies)) &
    (df["year"] >= year_start) &
    (df["year"] <= year_end)
]

st.subheader("Data Preview")
st.dataframe(df_filtered.round(2))

if show_roe:
    st.subheader("1. ROE Trend")
    fig1, ax1 = plt.subplots(figsize=(chart_width, 4))
    for c in companies:
        comp_data = df_filtered[df_filtered["tic"] == c]
        ax1.plot(comp_data["year"], comp_data["roe"], marker="o", label=c)
    ax1.legend()
    ax1.grid(True)
    st.pyplot(fig1)

st.subheader("2. Annual Revenue")
rev_data = df_filtered.pivot(index="year", columns="tic", values="sale")
st.bar_chart(rev_data)

if show_profit:
    st.subheader("3. Profit Margin Trend")
    fig3, ax3 = plt.subplots(figsize=(chart_width, 4))
    for c in companies:
        comp_data = df_filtered[df_filtered["tic"] == c]
        ax3.plot(comp_data["year"], comp_data["pm"], marker="s", label=c)
    ax3.legend()
    ax3.grid(True)
    st.pyplot(fig3)

if show_leverage:
    st.subheader("4. Leverage Level")
    lev_data = df_filtered.pivot(index="year", columns="tic", values="lev")
    st.area_chart(lev_data)

st.subheader("5. Financial Radar Chart (Latest Year)")

latest_year = df_filtered["year"].max()
latest_data = df_filtered[df_filtered["year"] == latest_year]

indicators = ["roe", "roa", "pm", "lev"]

def make_radar(data):
    angles = [i / len(indicators) * 2 * pi for i in range(len(indicators))]
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
