# ACC102 Financial Analysis Dashboard Project

## Project Introduction
This project is an interactive financial data visualization dashboard developed for the ACC102 course assignment.
The dataset is collected from **WRDS Compustat Database**, covering fiscal years **2020–2024** of four leading technology companies:
Apple (AAPL), Microsoft (MSFT), NVIDIA (NVDA), and Alphabet (GOOGL).

By calculating core financial ratios and using Streamlit to build a visual web dashboard,
this project achieves multi-company, multi-year, and multi-dimensional financial comparative analysis.

## Data Source
- Database: WRDS Compustat
- Time Period: 2020 – 2024
- Selected Companies: AAPL, MSFT, NVDA, GOOGL
- Raw Data Columns:
  - tic: Company ticker symbol
  - fyear: Fiscal year
  - sale: Total revenue
  - ni: Net income
  - at: Total assets
  - ceq: Total shareholder equity

## Financial Indicators Calculation
Four key financial ratios are computed in the program:
1. **ROE (Return on Equity)** = Net Income / Shareholder Equity
2. **ROA (Return on Assets)** = Net Income / Total Assets
3. **Profit Margin (PM)** = Net Income / Total Revenue
4. **Leverage (LEV)** = Total Assets / Shareholder Equity

## Dashboard Features
The Streamlit dashboard provides rich interactive functions:
- Select or deselect companies for comparison
- Adjust year range freely between 2020–2024
- Switch different financial indicators to observe trends
- Customize decimal places and chart width
- Show or hide raw data table and average trend line
- Choose X and Y variables for customized scatter plot analysis

## Visualization Charts
The project includes four professional financial charts:
1. **Line Chart**: Show financial ratio trends across years for all companies
2. **Scatter Plot**: Analyze correlation between different financial variables
3. **Bar Chart**: Compare annual revenue of four companies year by year
4. **Radar Chart**: Evaluate overall comprehensive financial performance of each company

