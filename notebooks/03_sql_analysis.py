# ============================================
# Project: Revenue Margin Analysis
# Script: 03_sql_analysis.py
# Purpose: Run SQL analysis using DuckDB
# ============================================

import duckdb
import pandas as pd

# Connect to DuckDB
# This creates a temporary in-memory database
con = duckdb.connect()

# Load our clean data into DuckDB as a table called 'sales'
# This lets us write SQL against it like a real database
con.execute("""
    CREATE TABLE sales AS 
    SELECT * FROM read_csv_auto('data/processed/superstore_clean.csv')
""")

print("✅ Data loaded into DuckDB")

# ============================================
# QUERY 1 — OVERALL REVENUE SUMMARY
# ============================================
# Business question: What is our overall financial performance?

print("\n" + "="*50)
print("QUERY 1: OVERALL REVENUE SUMMARY")
print("="*50)

q1 = con.execute("""
    SELECT
        COUNT(*)                                    AS total_transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Cost), 2)                        AS total_cost,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(AVG("Gross Margin %"), 2)            AS avg_margin_pct,
        ROUND(SUM("Discount Amount"), 2)           AS total_discount_given,
        SUM(CASE WHEN "Is Loss" = true 
            THEN 1 ELSE 0 END)                     AS loss_transactions
    FROM sales
""").df()

print(q1.to_string(index=False))

# ============================================
# QUERY 2 — MARGIN BY CATEGORY
# ============================================
# Business question: Which product categories are most and least profitable?

print("\n" + "="*50)
print("QUERY 2: MARGIN BY CATEGORY")
print("="*50)

q2 = con.execute("""
    SELECT
        Category,
        COUNT(*)                                    AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct,
        SUM(CASE WHEN "Is Loss" = true 
            THEN 1 ELSE 0 END)                     AS loss_transactions
    FROM sales
    GROUP BY Category
    ORDER BY margin_pct ASC
""").df()

print(q2.to_string(index=False))

# ============================================
# QUERY 3 — MARGIN BY SEGMENT
# ============================================
# Business question: Which customer segments are most profitable?

print("\n" + "="*50)
print("QUERY 3: MARGIN BY CUSTOMER SEGMENT")
print("="*50)

q3 = con.execute("""
    SELECT
        Segment,
        COUNT(*)                                    AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct,
        ROUND(AVG(Discount)*100, 2)                AS avg_discount_pct
    FROM sales
    GROUP BY Segment
    ORDER BY margin_pct ASC
""").df()

print(q3.to_string(index=False))

# ============================================
# QUERY 4 — DISCOUNT IMPACT ON MARGIN
# ============================================
# Business question: How much are discounts hurting our margin?

print("\n" + "="*50)
print("QUERY 4: DISCOUNT IMPACT ON MARGIN")
print("="*50)

q4 = con.execute("""
    SELECT
        CASE 
            WHEN Discount = 0          THEN '0% - No Discount'
            WHEN Discount <= 0.10      THEN '1-10% Discount'
            WHEN Discount <= 0.20      THEN '11-20% Discount'
            WHEN Discount <= 0.30      THEN '21-30% Discount'
            WHEN Discount <= 0.50      THEN '31-50% Discount'
            ELSE                            'Over 50% Discount'
        END                                        AS discount_bucket,
        COUNT(*)                                   AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct
    FROM sales
    GROUP BY discount_bucket
    ORDER BY margin_pct ASC
""").df()

print(q4.to_string(index=False))

# ============================================
# QUERY 5 — TOP LOSS MAKING SUB-CATEGORIES
# ============================================
# Business question: Which specific product types are losing money?

print("\n" + "="*50)
print("QUERY 5: TOP LOSS MAKING SUB-CATEGORIES")
print("="*50)

q5 = con.execute("""
    SELECT
        Category,
        "Sub-Category",
        COUNT(*)                                    AS transactions,
        ROUND(SUM(Sales), 2)                       AS total_revenue,
        ROUND(SUM(Profit), 2)                      AS total_profit,
        ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct,
        SUM(CASE WHEN "Is Loss" = true 
            THEN 1 ELSE 0 END)                     AS loss_transactions
    FROM sales
    GROUP BY Category, "Sub-Category"
    ORDER BY total_profit ASC
    LIMIT 10
""").df()

print(q5.to_string(index=False))

# ============================================
# SAVE RESULTS
# ============================================

q2.to_csv('data/processed/margin_by_category.csv', index=False)
q3.to_csv('data/processed/margin_by_segment.csv', index=False)
q4.to_csv('data/processed/discount_impact.csv', index=False)
q5.to_csv('data/processed/loss_subcategories.csv', index=False)

print("\n✅ All analysis results saved to data/processed/")

con.close()