-- 02_category_performance.sql
-- KPI: Revenue, order volume, and average review score by product category
-- Business question: Which categories drive the business, and which underperform on satisfaction?

SELECT
    COALESCE(p.product_category_name_english, 'unknown') AS category,
    COUNT(DISTINCT oi.order_id)                            AS order_count,
    ROUND(SUM(oi.price), 2)                                 AS product_revenue,
    ROUND(AVG(oi.price), 2)                                 AS avg_item_price,
    ROUND(AVG(r.review_score), 2)                           AS avg_review_score
FROM order_items oi
JOIN orders o       ON oi.order_id = o.order_id
LEFT JOIN products p ON oi.product_id = p.product_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY category
ORDER BY product_revenue DESC;
