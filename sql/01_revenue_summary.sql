-- ============================================
-- Revenue Summary
-- Business Question: What is our overall financial performance?
-- ============================================

SELECT
    COUNT(*)                                    AS total_transactions,
    ROUND(SUM(Sales), 2)                       AS total_revenue,
    ROUND(SUM(Cost), 2)                        AS total_cost,
    ROUND(SUM(Profit), 2)                      AS total_profit,
    ROUND(AVG("Gross Margin %"), 2)            AS avg_margin_pct,
    ROUND(SUM("Discount Amount"), 2)           AS total_discount_given,
    SUM(CASE WHEN "Is Loss" = true
        THEN 1 ELSE 0 END)                     AS loss_transactions
FROM sales;