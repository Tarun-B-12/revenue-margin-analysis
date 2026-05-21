# Revenue Leakage + Margin Analysis

## Live Dashboard
Interactive dashboard deployed on Streamlit Cloud:
https://revenue-margin-analysis-5ezuzkemmwudfqe6to9hsn.streamlit.app/

## GitHub Repository
https://github.com/Tarun-B-12/revenue-margin-analysis

## One-Line Summary
End-to-end margin analysis identifying $566k in revenue leakage across 9,994 transactions using Python, DuckDB, SQL, Streamlit, and Plotly.

## Business Problem
Many companies lose significant profit through excessive discounting, unprofitable product lines, and poorly targeted customer segments without realizing where the leakage is happening.

This project analyzes 9,994 retail transactions to identify exactly where margin is being lost, which discount thresholds destroy profitability, and which product categories and segments need immediate pricing attention.

## Target Stakeholder
- Sales Director
- Finance Manager
- VP of Operations
- Revenue Manager

## Tools Used
- Python with pandas for data loading, cleaning, and feature engineering
- DuckDB for in-memory SQL analysis engine
- SQL for business analysis queries
- Streamlit for interactive web dashboard
- Plotly for data visualizations
- GitHub for version control and portfolio showcase

## Dataset
- Source: Sample Superstore Dataset from Kaggle
- Records: 9,994 transactions
- Period: 2014 to 2017
- Fields: Orders, customers, products, sales, profit, discount, region, segment, category
- Note: Public dataset used for portfolio purposes. All metrics are project-level.

## Key Business Questions
1. What is the overall margin and where is profit leaking?
2. Which product categories are most and least profitable?
3. How much are discounts hurting margin?
4. Which customer segments drive the most and least profit?
5. Which specific sub-categories are actively losing money?
6. Which regions are underperforming on margin?
7. How has margin trended year over year?

## KPIs
| KPI | Definition | Why It Matters |
|---|---|---|
| Gross Margin % |

## Dashboard Screenshots

### KPI Overview
![KPI Overview](dashboards/screenshots/01_kpi_overview.png)

### Category and Discount Analysis
![Category Analysis](dashboards/screenshots/02_category_discount_analysis.png)

### Regional and Leakage Analysis
![Regional Analysis](dashboards/screenshots/03_regional_leakage_analysis.png)