-- ============================================
-- Regional Margin Analysis
-- Business Question: Which regions are underperforming on margin?
-- ============================================

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
ORDER BY margin_pct ASC;