-- ============================================
-- Margin by Category
-- Business Question: Which categories are most and least profitable?
-- ============================================

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
ORDER BY margin_pct ASC;