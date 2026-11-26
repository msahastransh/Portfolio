-- 01_monthly_revenue_trend.sql
-- KPI: Monthly Gross Merchandise Value (GMV), order count, and average order value (AOV)
-- Business question: How has revenue evolved month over month?
-- Note: analysis window restricted to 2017-01 through 2018-08; Sept-Dec 2016 and
-- Sept-Oct 2018 are excluded as near-empty pilot/tail periods (data quality decision,
-- see notebook Section 1.3 for the audit that justified this cut).

SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS year_month,
    COUNT(DISTINCT o.order_id)                     AS order_count,
    ROUND(SUM(oi.price + oi.freight_value), 2)      AS gmv,
    ROUND(SUM(oi.price), 2)                         AS product_revenue,
    ROUND(SUM(oi.freight_value), 2)                 AS freight_revenue,
    ROUND(SUM(oi.price + oi.freight_value) / COUNT(DISTINCT o.order_id), 2) AS avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY year_month
ORDER BY year_month;
