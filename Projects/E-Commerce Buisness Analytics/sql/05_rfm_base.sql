-- 05_rfm_base.sql
-- Base query for RFM (Recency, Frequency, Monetary) customer segmentation.
-- Uses customer_unique_id (not customer_id) since Olist assigns a new customer_id
-- per order — customer_unique_id is the true repeat-customer identifier.
-- Business question: Who are our most valuable customers, and who is at risk of churn?

SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS frequency,
    ROUND(SUM(oi.price + oi.freight_value), 2) AS monetary,
    MAX(o.order_purchase_timestamp) AS last_purchase_date,
    MIN(o.order_purchase_timestamp) AS first_purchase_date
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY c.customer_unique_id;
