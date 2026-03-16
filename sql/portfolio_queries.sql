-- ================================================
-- PUBLIC SECTOR LOAN PORTFOLIO ANALYTICS
-- Author: Babatunde Atunbi
-- Description: Core portfolio monitoring queries
-- ================================================

-- TABLES
-- BORROWERS TABLE
CREATE TABLE borrowers (
    borrower_id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    employer VARCHAR(100),
    monthly_salary NUMERIC(15,2),
    state VARCHAR(50),
    employment_type VARCHAR(50),
    date_onboarded DATE
);

-- LOANS TABLE
CREATE TABLE loans (
    loan_id SERIAL PRIMARY KEY,
    borrower_id INT REFERENCES borrowers(borrower_id),
    loan_amount NUMERIC(15,2),
    loan_purpose VARCHAR(100),
    interest_rate NUMERIC(5,2),
    tenure_months INT,
    disbursement_date DATE,
    maturity_date DATE,
    monthly_repayment NUMERIC(15,2),
    loan_status VARCHAR(50)
);

-- REPAYMENTS TABLE 
CREATE TABLE repayments (
    repayment_id SERIAL PRIMARY KEY,
    loan_id INT REFERENCES loans(loan_id),
    borrower_id INT REFERENCES borrowers(borrower_id),
    due_date DATE,
    actual_payment_date DATE,
    amount_due NUMERIC(15,2),
    amount_paid NUMERIC(15,2),
    payment_status VARCHAR(50)
);

-- DPD CLASSIFICATION TABLE
CREATE TABLE dpd_classifications (
    dpd_id SERIAL PRIMARY KEY,
    loan_id INT REFERENCES loans(loan_id),
    borrower_id INT REFERENCES borrowers(borrower_id),
    calculation_date DATE,
    days_past_due INT,
    dpd_bucket VARCHAR(20),
    outstanding_balance NUMERIC(15,2),
    classification VARCHAR(50)
);



-- 1. PORTFOLIO SUMMARY BY LOAN STATUS
SELECT 
    loan_status,
    COUNT(*) AS number_of_loans,
    SUM(loan_amount) AS total_loan_amount,
    ROUND(AVG(loan_amount), 2) AS average_loan_amount,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS portfolio_percentage
FROM loans
GROUP BY loan_status
ORDER BY total_loan_amount DESC;

-- 2. DPD BUCKET ANALYSIS
SELECT 
    dpd_bucket,
    classification,
    COUNT(*) AS number_of_loans,
    SUM(outstanding_balance) AS total_outstanding,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage_of_portfolio
FROM dpd_classifications
GROUP BY dpd_bucket, classification
ORDER BY 
    CASE dpd_bucket
        WHEN 'Current' THEN 1
        WHEN '1-30 DPD' THEN 2
        WHEN '31-60 DPD' THEN 3
        WHEN '61-90 DPD' THEN 4
        WHEN '90+ DPD' THEN 5
    END;

-- 3. PAR RATIOS
SELECT
    ROUND(100.0 * SUM(CASE WHEN days_past_due > 0 THEN outstanding_balance ELSE 0 END) /
    SUM(outstanding_balance), 2) AS PAR1,
    ROUND(100.0 * SUM(CASE WHEN days_past_due > 30 THEN outstanding_balance ELSE 0 END) /
    SUM(outstanding_balance), 2) AS PAR30,
    ROUND(100.0 * SUM(CASE WHEN days_past_due > 60 THEN outstanding_balance ELSE 0 END) /
    SUM(outstanding_balance), 2) AS PAR60,
    ROUND(100.0 * SUM(CASE WHEN days_past_due > 90 THEN outstanding_balance ELSE 0 END) /
    SUM(outstanding_balance), 2) AS PAR90
FROM dpd_classifications;

-- 4. CONCENTRATION RISK BY EMPLOYER AND STATE
SELECT 
    b.employer,
    b.state,
    COUNT(l.loan_id) AS number_of_loans,
    SUM(l.loan_amount) AS total_exposure,
    ROUND(100.0 * SUM(l.loan_amount) / SUM(SUM(l.loan_amount)) OVER (), 2) AS exposure_percentage,
    SUM(CASE WHEN l.loan_status = 'Delinquent' THEN 1 ELSE 0 END) AS delinquent_loans,
    ROUND(100.0 * SUM(CASE WHEN l.loan_status = 'Delinquent' THEN 1 ELSE 0 END) / COUNT(l.loan_id), 2) AS delinquency_rate
FROM loans l
JOIN borrowers b ON l.borrower_id = b.borrower_id
GROUP BY b.employer, b.state
ORDER BY total_exposure DESC
LIMIT 10;

-- 5. REPAYMENT PERFORMANCE AND COLLECTION RATE
SELECT
    b.employer,
    COUNT(DISTINCT r.loan_id) AS number_of_loans,
    SUM(r.amount_due) AS total_amount_due,
    SUM(r.amount_paid) AS total_amount_collected,
    ROUND(100.0 * SUM(r.amount_paid) / SUM(r.amount_due), 2) AS collection_rate,
    SUM(r.amount_due - r.amount_paid) AS total_shortfall,
    COUNT(CASE WHEN r.payment_status = 'Missed' THEN 1 END) AS missed_payments,
    COUNT(CASE WHEN r.payment_status = 'Late' THEN 1 END) AS late_payments,
    COUNT(CASE WHEN r.payment_status = 'Paid' THEN 1 END) AS on_time_payments
FROM repayments r
JOIN loans l ON r.loan_id = l.loan_id
JOIN borrowers b ON l.borrower_id = b.borrower_id
GROUP BY b.employer
ORDER BY collection_rate ASC;