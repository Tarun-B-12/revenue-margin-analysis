# Revenue Leakage + Margin Analysis

## One-Line Summary
End-to-end margin analysis identifying revenue leakage across products, categories, and customer segments using Python, SQL, and Tableau.

## Business Problem
Many companies lose significant profit through excessive discounting, unprofitable product lines, and poorly targeted customer segments — without realizing where the leakage is happening.

This project analyzes 9,994 retail transactions to identify exactly where margin is being lost, which discount thresholds destroy profitability, and which product categories and segments need immediate pricing attention.

## Target Stakeholder
- Sales Director
- Finance Manager
- VP of Operations
- Revenue Manager

## Tools Used
- Python (pandas) — data loading, cleaning, feature engineering
- DuckDB — in-memory SQL analysis engine
- SQL — business analysis queries
- Tableau Public — interactive dashboard
- GitHub — version control and portfolio showcase

## Dataset
- Source: Sample Superstore Dataset (Kaggle)
- Records: 9,994 transactions
- Period: 2014 to 2017
- Fields: Orders, customers, products, sales, profit, discount, region, segment, category

## Key Business Questions
1. What is the overall margin and where is profit leaking?
2. Which product categories are most and least profitable?
3. How much are discounts hurting margin?
4. Which customer segments drive the most and least profit?
5. Which specific sub-categories are actively losing money?

## KPIs
| KPI | Definition | Why It Matters |
|---|---|---|
| Gross Margin % | Profit / Sales × 100 | Core profitability measure |
| Total Revenue | Sum of all sales | Business scale |
| Total Profit | Sum of all profit | Actual earnings |
| Discount Rate % | Discount / Original Price × 100 | Pricing discipline |
| Loss Transactions | Count of orders where Profit < 0 | Risk exposure |
| Revenue at Risk | Revenue from transactions below 10% margin | Leakage opportunity |

## Project Architecture
Raw CSV → Python Cleaning → DuckDB SQL Analysis → Processed CSVs → Tableau Dashboard

## Key Findings

### Finding 1 — Discounts Exceed Earnings
The business gave away **$566,734 in discounts** while earning only **$286,397 in profit**. Discounting is outpacing profitability.

### Finding 2 — Discount Rate Destroys Margin
| Discount Level | Margin |
|---|---|
| No Discount | +29.51% |
| 1-10% | +16.61% |
| 11-20% | +11.58% |
| 21-30% | -10.05% |
| 31-50% | -24.80% |
| Over 50% | -119.20% |

Any discount above 20% results in losses.

### Finding 3 — Furniture Is a Loss Leader
Furniture generated $742k in revenue but only $18k in profit — a 2.49% margin. Tables alone lost $17,725 with 63% of transactions unprofitable.

### Finding 4 — Segment Profitability Gap
| Segment | Margin |
|---|---|
| Home Office | 14.03% |
| Corporate | 13.03% |
| Consumer | 11.55% |

Consumer is the largest segment but the least profitable.

## Business Recommendations
1. Set a hard discount cap at 20% — any discount above this level produces negative margin
2. Reprice or discontinue the Tables sub-category — 63% of transactions lose money
3. Prioritize Home Office and Corporate segments over Consumer for high-value deals
4. Review Furniture category pricing strategy — 2.49% margin is not sustainable

## Data Cleaning Steps
- Converted Order Date and Ship Date from string to datetime
- Extracted year, month, quarter from order dates
- Added Gross Margin % column
- Added Cost column
- Added Discount Amount in dollars
- Flagged loss transactions where Profit < 0
- Flagged high discount transactions where Discount > 30%
- Flagged low margin transactions where Margin < 10%

## What This Project Demonstrates
- Business problem framing and stakeholder thinking
- Python data cleaning and feature engineering
- SQL analysis using DuckDB
- KPI definition and metric design
- Revenue leakage identification
- Dashboard design and data storytelling
- GitHub documentation and portfolio packaging

## Limitations
- Dataset is sample/public retail data — not from a real company
- Metrics are project-level and based on public data
- No seasonality or external market data included
- Cost structure assumptions are based on Sales minus Profit

## Repository Structure
revenue-margin-analysis/
data/
raw/          ← original dataset
processed/    ← cleaned and analysis output files
notebooks/      ← Python scripts for exploration and cleaning
sql/            ← SQL query files
dashboards/
screenshots/  ← Tableau dashboard screenshots
docs/           ← data dictionary and notes
README.md
requirements.txt

## Next Improvements
- Add forecasting layer to predict future margin by category
- Add automated data refresh pipeline
- Deploy interactive Tableau dashboard with live filters
- Add statistical significance testing on discount impact