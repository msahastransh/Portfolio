-- 04_payment_behavior.sql
-- KPI: Payment method mix and installment behavior
-- Business question: How do customers prefer to pay, and does installment count relate to order value?

SELECT
    op.payment_type,
    COUNT(*) AS payment_count,
    ROUND(AVG(op.payment_value), 2) AS avg_payment_value,
    ROUND(AVG(op.payment_installments), 1) AS avg_installments,
    ROUND(SUM(op.payment_value), 2) AS total_payment_value
FROM order_payments op
JOIN orders o ON op.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp >= '2017-01-01'
  AND o.order_purchase_timestamp < '2018-09-01'
GROUP BY op.payment_type
ORDER BY total_payment_value DESC;
