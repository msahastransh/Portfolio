-- 07_delivery_vs_satisfaction.sql
-- KPI: Relationship between delivery timeliness and customer review score
-- Business question: Does late delivery hurt customer satisfaction, and by how much?

SELECT
    CASE
        WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) <= -7 THEN '1. Early (7+ days)'
        WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) <= 0  THEN '2. On time'
        WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) <= 7  THEN '3. Late (1-7 days)'
        ELSE '4. Very late (7+ days)'
    END AS delivery_bucket,
    COUNT(*) AS order_count,
    ROUND(AVG(r.review_score), 3) AS avg_review_score,
    ROUND(100.0 * SUM(CASE WHEN r.review_score <= 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS pct_negative_reviews
FROM orders o
JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY delivery_bucket
ORDER BY delivery_bucket;
