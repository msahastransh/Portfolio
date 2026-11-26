-- 09_marketing_funnel_conversion.sql
-- KPI: Marketing Qualified Lead (MQL) -> Closed Deal conversion rate, by lead origin
-- Business question: Which acquisition channels convert leads into sellers most effectively?

SELECT
    COALESCE(lq.origin, 'unknown') AS lead_origin,
    COUNT(DISTINCT lq.mql_id) AS total_leads,
    COUNT(DISTINCT lc.mql_id) AS closed_deals,
    ROUND(100.0 * COUNT(DISTINCT lc.mql_id) / COUNT(DISTINCT lq.mql_id), 2) AS conversion_rate_pct
FROM leads_qualified lq
LEFT JOIN leads_closed lc ON lq.mql_id = lc.mql_id
GROUP BY lead_origin
ORDER BY total_leads DESC;
