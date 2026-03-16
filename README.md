# Public Sector Loan Portfolio Analytics System

## Overview
An end-to-end loan portfolio analytics project simulating a public sector retail lending book. Built to demonstrate practical skills in SQL, Python, Power BI, and Excel for portfolio monitoring, risk reporting, and credit decisioning.

## Project Structure
```
loan_portfolio_project/
│
├── sql/                          # Core portfolio analytics queries
├── data/                         # Python data generation script
├── notebooks/                    # Python analysis notebook
└── dashboard/                    # Power BI dashboard & Excel report
```

## Key Analyses
- Portfolio summary by loan status
- DPD bucket classification (Current → 90+ days)
- PAR1, PAR30, PAR60, PAR90 ratio calculations
- Employer and state concentration risk analysis
- Repayment performance and collection rate by employer

## Tools Used
| Tool | Purpose |
|------|---------|
| PostgreSQL | Database design and querying |
| Python (pandas, sqlalchemy, matplotlib) | Data generation and analysis |
| Power BI | Interactive 4-page dashboard |
| Excel | Formatted analytics report |

## Key Findings (Simulated Data)
- Total portfolio value: NGN 524M across 200 borrowers
- PAR1 at 37% — significantly above the 10% benchmark for public sector lending
- NNPC has the lowest collection rate at 67.64%
- Nigerian Army has the highest collection rate at 92.03%
- 27.5% of the portfolio is stressed (delinquent or written off)

## Author
**Babatunde Atunbi** — Portfolio Analytics | MIS & Risk Reporting | Financial Data Analysis
[LinkedIn](https://linkedin.com/in/atvnbi) | atunbitunde1@gmail.com