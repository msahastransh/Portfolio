-- 10_order_status_funnel.sql
-- KPI: Full order status breakdown (all statuses, unfiltered) and cancellation rate over time
-- Business question: What share of orders fail to complete, and is this trend improving or worsening?

SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS year_month,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN order_status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) AS canceled,
    SUM(CASE WHEN order_status = 'unavailable' THEN 1 ELSE 0 END) AS unavailable,
    ROUND(100.0 * SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_rate_pct
FROM orders
WHERE order_purchase_timestamp >= '2017-01-01'
  AND order_purchase_timestamp < '2018-09-01'
GROUP BY year_month
ORDER BY year_month;
