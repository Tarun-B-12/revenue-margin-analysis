-- ============================================
-- Revenue Leakage Summary
-- Business Question: What is the total scale of revenue leakage?
-- ============================================

SELECT 'Total Revenue'                             AS metric,
    ROUND(SUM(Sales), 2)                           AS value
FROM sales

UNION ALL

SELECT 'Total Profit',
    ROUND(SUM(Profit), 2)
FROM sales

UNION ALL

SELECT 'Total Discount Given',
    ROUND(SUM("Discount Amount"), 2)
FROM sales

UNION ALL

SELECT 'Revenue From Loss Transactions',
    ROUND(SUM(Sales), 2)
FROM sales
WHERE "Is Loss" = true

UNION ALL

SELECT 'Profit Destroyed by Loss Transactions',
    ROUND(SUM(Profit), 2)
FROM sales
WHERE "Is Loss" = true

UNION ALL

SELECT 'Revenue at Risk From Low Margin Transactions',
    ROUND(SUM(Sales), 2)
FROM sales
WHERE "Is Low Margin" = true;