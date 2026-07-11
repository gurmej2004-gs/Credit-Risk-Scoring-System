-- ============================================
-- SQL Analytics Queries for Credit Risk System
-- ============================================

USE credit_risk_db;

-- ============================================
-- 1. Total Customers
-- ============================================
SELECT COUNT(*) AS total_customers
FROM customers;

-- ============================================
-- 2. Average Monthly Income
-- ============================================
SELECT AVG(monthly_income) AS avg_income
FROM customers;

-- ============================================
-- 3. High Risk Customers
-- ============================================
SELECT *
FROM risk_scores
WHERE risk_category = 'High Risk';

-- ============================================
-- 4. Risk Category Distribution
-- ============================================
SELECT risk_category,
       COUNT(*) AS total
FROM risk_scores
GROUP BY risk_category;

-- ============================================
-- 5. Lowest Risk Scores
-- ============================================
SELECT customer_id,
       risk_score
FROM risk_scores
ORDER BY risk_score ASC
LIMIT 10;

-- ============================================
-- 6. Average Debt Ratio
-- ============================================
SELECT AVG(debt_ratio) AS avg_debt_ratio
FROM credit_profile;

-- ============================================
-- 7. Customers With More Than 3 Dependents
-- ============================================
SELECT *
FROM customers
WHERE dependents > 3;

-- ============================================
-- 8. Customers With Income Above 50000
-- ============================================
SELECT *
FROM customers
WHERE monthly_income > 50000;

-- ============================================
-- 9. Top 10 Highest Income Customers
-- ============================================
SELECT customer_id,
       monthly_income
FROM customers
ORDER BY monthly_income DESC
LIMIT 10;

-- ============================================
-- 10. Risk Score Statistics
-- ============================================
SELECT 
    MIN(risk_score) AS min_risk_score,
    MAX(risk_score) AS max_risk_score,
    AVG(risk_score) AS avg_risk_score,
    COUNT(*) AS total_customers
FROM risk_scores;

-- ============================================
-- 11. Low Risk Customers
-- ============================================
SELECT *
FROM risk_scores
WHERE risk_category = 'Low Risk'
ORDER BY risk_score DESC
LIMIT 10;

-- ============================================
-- 12. Medium Risk Customers
-- ============================================
SELECT *
FROM risk_scores
WHERE risk_category = 'Medium Risk'
ORDER BY risk_score DESC
LIMIT 10;

-- ============================================
-- 13. Average Credit Utilization by Risk Category
-- ============================================
SELECT 
    rs.risk_category,
    AVG(cp.credit_utilization) AS avg_credit_utilization
FROM risk_scores rs
JOIN credit_profile cp ON rs.customer_id = cp.customer_id
GROUP BY rs.risk_category
ORDER BY rs.risk_category;

-- ============================================
-- 14. Average Debt Ratio by Risk Category
-- ============================================
SELECT 
    rs.risk_category,
    AVG(cp.debt_ratio) AS avg_debt_ratio
FROM risk_scores rs
JOIN credit_profile cp ON rs.customer_id = cp.customer_id
GROUP BY rs.risk_category
ORDER BY rs.risk_category;

-- ============================================
-- 15. Customers with Late Payments by Risk Category
-- ============================================
SELECT 
    rs.risk_category,
    COUNT(CASE WHEN ph.late_30_59 > 0 THEN 1 END) AS customers_late_30_59,
    COUNT(CASE WHEN ph.late_60_89 > 0 THEN 1 END) AS customers_late_60_89,
    COUNT(CASE WHEN ph.late_90 > 0 THEN 1 END) AS customers_late_90
FROM risk_scores rs
JOIN payment_history ph ON rs.customer_id = ph.customer_id
GROUP BY rs.risk_category
ORDER BY rs.risk_category;

-- ============================================
-- 16. Age Distribution
-- ============================================
SELECT 
    CASE 
        WHEN age < 25 THEN 'Under 25'
        WHEN age BETWEEN 25 AND 34 THEN '25-34'
        WHEN age BETWEEN 35 AND 44 THEN '35-44'
        WHEN age BETWEEN 45 AND 54 THEN '45-54'
        WHEN age BETWEEN 55 AND 64 THEN '55-64'
        ELSE '65+'
    END AS age_group,
    COUNT(*) AS total_customers
FROM customers
GROUP BY age_group
ORDER BY age_group;

-- ============================================
-- 17. Income Distribution by Risk Category
-- ============================================
SELECT 
    rs.risk_category,
    AVG(c.monthly_income) AS avg_income,
    MIN(c.monthly_income) AS min_income,
    MAX(c.monthly_income) AS max_income
FROM risk_scores rs
JOIN customers c ON rs.customer_id = c.customer_id
GROUP BY rs.risk_category
ORDER BY rs.risk_category;

-- ============================================
-- 18. Complete Customer Profile with Risk Score
-- ============================================
SELECT 
    c.customer_id,
    c.age,
    c.monthly_income,
    c.dependents,
    cp.debt_ratio,
    cp.credit_utilization,
    ph.late_30_59,
    ph.late_60_89,
    ph.late_90,
    rs.risk_score,
    rs.risk_category
FROM customers c
JOIN credit_profile cp ON c.customer_id = cp.customer_id
JOIN payment_history ph ON c.customer_id = ph.customer_id
JOIN risk_scores rs ON c.customer_id = rs.customer_id
ORDER BY rs.risk_score DESC
LIMIT 20;
