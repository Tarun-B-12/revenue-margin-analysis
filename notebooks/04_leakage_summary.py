# ============================================
# Project: Revenue Margin Analysis
# Script: 04_leakage_summary.py
# Purpose: Regional analysis and leakage summary
# ============================================

import duckdb
import pandas as pd

con = duckdb.connect()

con.execute("""
    CREATE TABLE sales AS
    SELECT * FROM read_csv_auto('data/processed/superstore_clean.csv')
""")

print("✅ Data loaded into DuckDB")

# ============================================
# QUERY 6 — MARGIN BY REGION
# ============================================

print("\n" + "="*50)
print("QUERY 6: MARGIN BY REGION")
print("="*50)

q6 = con.execute("""
    SELECT
        Region,
        COUNT(*)                                    AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct,
        SUM(CASE WHEN "Is Loss" = true
            THEN 1 ELSE 0 END)                     AS loss_transactions,
        ROUND(AVG(Discount)*100, 2)                AS avg_discount_pct
    FROM sales
    GROUP BY Region
    ORDER BY margin_pct ASC
""").df()

print(q6.to_string(index=False))

# ============================================
# QUERY 7 — YEARLY MARGIN TREND
# ============================================

print("\n" + "="*50)
print("QUERY 7: YEARLY MARGIN TREND")
print("="*50)

q7 = con.execute("""
    SELECT
        "Order Year"                                AS year,
        COUNT(*)                                    AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct,
        ROUND(SUM("Discount Amount"), 2)           AS total_discount_given
    FROM sales
    GROUP BY "Order Year"
    ORDER BY year ASC
""").df()

print(q7.to_string(index=False))

# ============================================
# QUERY 8 — FULL LEAKAGE SUMMARY
# ============================================

print("\n" + "="*50)
print("QUERY 8: REVENUE LEAKAGE SUMMARY")
print("="*50)

q8 = con.execute("""
    SELECT
        'Total Revenue'                            AS metric,
        ROUND(SUM(Sales), 2)                       AS value
    FROM sales

    UNION ALL

    SELECT
        'Total Profit',
        ROUND(SUM(Profit), 2)
    FROM sales

    UNION ALL

    SELECT
        'Total Discount Given',
        ROUND(SUM("Discount Amount"), 2)
    FROM sales

    UNION ALL

    SELECT
        'Revenue From Loss Transactions',
        ROUND(SUM(Sales), 2)
    FROM sales
    WHERE "Is Loss" = true

    UNION ALL

    SELECT
        'Profit Lost From Loss Transactions',
        ROUND(SUM(Profit), 2)
    FROM sales
    WHERE "Is Loss" = true

    UNION ALL

    SELECT
        'Revenue From High Discount Transactions',
        ROUND(SUM(Sales), 2)
    FROM sales
    WHERE "Is High Discount" = true

    UNION ALL

    SELECT
        'Revenue From Low Margin Transactions',
        ROUND(SUM(Sales), 2)
    FROM sales
    WHERE "Is Low Margin" = true
""").df()

print(q8.to_string(index=False))

# ============================================
# SAVE RESULTS
# ============================================

q6.to_csv('data/processed/margin_by_region.csv', index=False)
q7.to_csv('data/processed/yearly_trend.csv', index=False)
q8.to_csv('data/processed/leakage_summary.csv', index=False)

print("\n✅ All leakage analysis saved to data/processed/")

con.close()