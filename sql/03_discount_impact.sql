-- ============================================
-- Discount Impact on Margin
-- Business Question: How much are discounts hurting margin?
-- ============================================

SELECT
    CASE
        WHEN Discount = 0          THEN '0% No Discount'
        WHEN Discount <= 0.10      THEN '1 to 10% Discount'
        WHEN Discount <= 0.20      THEN '11 to 20% Discount'
        WHEN Discount <= 0.30      THEN '21 to 30% Discount'
        WHEN Discount <= 0.50      THEN '31 to 50% Discount'
        ELSE                            'Over 50% Discount'
    END                                        AS discount_bucket,
    COUNT(*)                                   AS transactions,
    ROUND(SUM(Sales), 2)                       AS total_revenue,
    ROUND(SUM(Profit), 2)                      AS total_profit,
    ROUND(SUM(Profit)/SUM(Sales)*100, 2)       AS margin_pct
FROM sales
GROUP BY discount_bucket
ORDER BY margin_pct ASC;