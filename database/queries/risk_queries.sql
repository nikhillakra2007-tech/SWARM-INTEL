-- risk_queries.sql — Risk scoring & history queries

-- Latest risk per customer
SELECT c.customer_ref, rs.risk_score, rs.risk_level, rs.calculated_at
FROM customers c
JOIN LATERAL (
  SELECT * FROM risk_scores rs WHERE rs.entity_type='CUSTOMER' AND rs.entity_id=c.customer_id ORDER BY calculated_at DESC LIMIT 1
) rs ON true
ORDER BY rs.risk_score DESC;

-- Risk trend for a single customer (C013)
SELECT risk_score, risk_level, calculated_at FROM risk_scores
WHERE entity_type='CUSTOMER' AND entity_id=(SELECT customer_id FROM customers WHERE customer_ref='C013')
ORDER BY calculated_at;

-- Average risk by dealer
SELECT d.dealer_code, avg(rs.risk_score)::numeric(5,2) AS avg_risk
FROM dealers d JOIN loan_applications la ON la.dealer_id=d.dealer_id
JOIN risk_scores rs ON rs.entity_type='CUSTOMER' AND rs.entity_id=la.customer_id
GROUP BY d.dealer_id ORDER BY avg_risk DESC;
