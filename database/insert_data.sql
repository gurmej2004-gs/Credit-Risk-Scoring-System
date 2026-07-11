-- ============================================
-- Insert Data into Credit Risk Database
-- ============================================
-- This file will be generated dynamically by database_loader.py
-- ============================================

USE credit_risk_db;

-- ============================================
-- Insert into customers table
-- ============================================
-- INSERT INTO customers (customer_id, age, monthly_income, dependents)
-- VALUES 
--     (1, 45, 50000.00, 2),
--     (2, 32, 35000.00, 1),
--     ...

-- ============================================
-- Insert into credit_profile table
-- ============================================
-- INSERT INTO credit_profile (customer_id, debt_ratio, credit_utilization, open_credit_lines, real_estate_loans)
-- VALUES 
--     (1, 0.45, 0.30, 5, 1),
--     (2, 0.60, 0.85, 3, 0),
--     ...

-- ============================================
-- Insert into payment_history table
-- ============================================
-- INSERT INTO payment_history (customer_id, late_30_59, late_60_89, late_90)
-- VALUES 
--     (1, 0, 0, 0),
--     (2, 1, 0, 0),
--     ...

-- ============================================
-- Insert into risk_scores table
-- ============================================
-- INSERT INTO risk_scores (customer_id, risk_score, risk_category)
-- VALUES 
--     (1, 90, 'Low Risk'),
--     (2, 65, 'Medium Risk'),
--     ...
