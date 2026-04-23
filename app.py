import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import wrds

st.set_page_config(page_title="ACC102 WRDS Dashboard", layout="wide")
st.title("Interactive Financial Analysis Tool")
st.caption("Data Source: WRDS Compustat (2010–2024)")

# Sidebar
st.sidebar.header("WRDS Login")
username = st.sidebar.text_input("WRDS Username")
password = st.sidebar.text_input("WRDS Password", type="password")

# 5 companies
company_list = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
selected_companies = st.sidebar.multiselect("Select Companies", company_list, default=company_list)

# Year range
start_year = st.sidebar.slider("Start Year", 2010, 2023, 2015)
end_year = st.sidebar.slider("End Year", 2015, 2024, 2024)

# Indicators
indicators = st.sidebar.multiselect(
    "Indicators",
    ["ROE", "ROA", "Leverage", "Profit Margin"],
    default=["ROE", "ROA", "Leverage"]
)

indicator_map = {
    "ROE": "roe",
    "ROA": "roa",
    "Leverage": "lev",
    "Profit Margin": "pm"
}

# Load data from WRDS
@st.cache_data(ttl=3600)
def get_wrds_data(usr, pwd, tickers, sy, ey):
    try:
        db = wrds.Connection(wrds_username=usr, wrds_password=pwd)
        tickers_str = ",".join([f"'{t}'" for t in tickers])
        sql = f"""
            SELECT tic, conm, datadate, ni, sale, at, lt, roe
            FROM comp.funda
            WHERE tic IN ({tickers_str})
            AND EXTRACT(YEAR FROM datadate) BETWEEN {sy} AND {ey}
            AND datafmt='STD' AND consol='C' AND indfmt='INDL'
            ORDER BY tic, datadate;
        """
        df = db.raw_sql(sql)
        db.close()
        return df
    except Exception as e:
        st.error(f"WRDS Connection Error: {e}")
        return None

if st.sidebar.button("Load Data from WRDS"):
    if not username or not password:
        st.warning("Please enter your WRDS account first!")
        st.stop()
    
    with st.spinner("Fetching data from WRDS..."):
        df = get_wrds_data(username, password, selected_companies, start_year, end_year)
    
    if df is None or df.empty:
        st.error("No data retrieved.")
        st.stop()
    
    # Data cleaning
    df["year"] = pd.to_datetime(df["datadate"]).dt.year
    df = df.dropna(subset=["at", "sale"])
    df["roa"] = df["ni"] / df["at"]
    df["lev"] = df["lt"] / df["at"]
    df["pm"] = df["ni"] / df["sale"]
    
    st.session_state["df"] = df
    st.success("Data loaded successfully from WRDS!")

# Display
if "df" in st.session_state:
    df = st.session_state["df"]
    
    st.subheader("Raw Data Preview")
    st.dataframe(df.round(3))

    # Trend charts
    st.subheader("Indicator Trends")
    selected_cols = [indicator_map[i] for i in indicators]
    
    n = len(selected_cols)
    fig, axes = plt.subplots(n, 1, figsize=(10, 4 * n))
    if n == 1:
        axes = [axes]
    
    for i, col in enumerate(selected_cols):
        for tic in df["tic"].unique():
            sub = df[df["tic"] == tic]
            axes[i].plot(sub["year"], sub[col], marker="o", label=tic)
        axes[i].set_title(col.upper())
        axes[i].legend()
        axes[i].grid(True)
    
    plt.tight_layout()
    st.pyplot(fig)

    # Revenue bar chart
    st.subheader("Annual Revenue Comparison")
    revenue_pivot = df.pivot(index="year", columns="tic", values="sale")
    st.bar_chart(revenue_pivot)

    # Latest year summary
    st.subheader("Latest Year Performance")
    max_year = df["year"].max()
    latest = df[df["year"] == max_year].set_index("tic")
    st.dataframe(latest[["conm", "roe", "roa", "lev", "pm"]].round(3))
