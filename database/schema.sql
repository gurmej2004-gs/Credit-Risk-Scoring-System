-- ============================================
-- Credit Risk Scoring Database Schema
-- ============================================

-- Create Database
CREATE DATABASE IF NOT EXISTS credit_risk_db;
USE credit_risk_db;

-- ============================================
-- Table: customers
-- Stores basic customer information
-- ============================================
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    age INT NOT NULL,
    monthly_income DECIMAL(15, 2) NOT NULL,
    dependents INT NOT NULL DEFAULT 0,
    INDEX idx_age (age),
    INDEX idx_income (monthly_income)
);

-- ============================================
-- Table: credit_profile
-- Stores credit-related information
-- ============================================
CREATE TABLE IF NOT EXISTS credit_profile (
    customer_id INT PRIMARY KEY,
    debt_ratio DECIMAL(10, 4) NOT NULL,
    credit_utilization DECIMAL(10, 4) NOT NULL,
    open_credit_lines INT NOT NULL,
    real_estate_loans INT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_debt_ratio (debt_ratio),
    INDEX idx_credit_utilization (credit_utilization)
);

-- ============================================
-- Table: payment_history
-- Stores late payment history
-- ============================================
CREATE TABLE IF NOT EXISTS payment_history (
    customer_id INT PRIMARY KEY,
    late_30_59 INT NOT NULL DEFAULT 0,
    late_60_89 INT NOT NULL DEFAULT 0,
    late_90 INT NOT NULL DEFAULT 0,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_late_30_59 (late_30_59),
    INDEX idx_late_60_89 (late_60_89),
    INDEX idx_late_90 (late_90)
);

-- ============================================
-- Table: risk_scores
-- Stores calculated risk scores and categories
-- ============================================
CREATE TABLE IF NOT EXISTS risk_scores (
    customer_id INT PRIMARY KEY,
    risk_score INT NOT NULL,
    risk_category VARCHAR(20) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    INDEX idx_risk_score (risk_score),
    INDEX idx_risk_category (risk_category)
);

-- ============================================
-- Display table information
-- ============================================
SHOW TABLES;
