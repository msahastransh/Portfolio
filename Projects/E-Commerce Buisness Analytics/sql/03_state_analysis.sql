-- 03_state_analysis.sql
-- KPI: Order volume, revenue, and average delivery time by customer state
-- Business question: Where are our customers, and does geography affect delivery performance?

SELECT
    c.customer_state AS state,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS gmv,
    ROUND(AVG(oi.freight_value), 2) AS avg_freight_value,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp)), 1) AS avg_delivery_days,
    ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)), 1) AS avg_days_vs_estimate
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY state
ORDER BY gmv DESC;
