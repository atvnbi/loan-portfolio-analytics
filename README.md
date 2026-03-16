# Public Sector Loan Portfolio Analytics System

## Overview
An end-to-end loan portfolio analytics system simulating a public sector retail lending book. Built to bridge the gap between domain expertise in credit risk and the technical capability to automate, visualise, and scale the workflows that most analysts handle through Excel and core banking system reports.

This project reflects real workflows from managing live public sector lending portfolios worth NGN 600M to NGN 4B+, rebuilt with a proper technical stack.

## Project Structure
```
loan_portfolio_project/
│
├── sql/                          # Core portfolio analytics queries
├── data/                         # Python data generation script
├── notebooks/                    # Python analysis notebook
└── dashboard/                    # Power BI dashboard & Excel report
```

## Tech Stack
| Tool | Purpose |
|------|---------|
| PostgreSQL | Relational database — borrowers, loans, repayments, DPD classifications |
| Python (pandas, SQLAlchemy, matplotlib) | Data generation, analysis, and automation |
| Power BI | Interactive 4-page dashboard |
| Excel | Formatted 5-sheet analytics report |

## Key Analyses
1. **Portfolio Summary** — loan status breakdown, total exposure, average loan size
2. **DPD Bucket Analysis** — classification from Current through 90+ days past due
3. **PAR Ratios** — PAR1, PAR30, PAR60, PAR90 vs industry benchmarks
4. **Concentration Risk** — exposure and delinquency rate by employer and state
5. **Repayment Performance** — collection rates, payment breakdown, and shortfall by employer

## Key Findings (Simulated Data)
- Total portfolio value: NGN 524M across 200 public sector borrowers
- PAR1 at 37% — more than 3x the 10% benchmark for salary-backed public sector lending
- 27.5% of the portfolio is stressed — delinquent or written off
- NNPC recorded the lowest collection rate at 67.64%
- Nigerian Army recorded the highest collection rate at 92.03%
- Total repayment shortfall: NGN 140M+
- Concentration risk identified in NNPC, CBN, and Lagos State Government — pointing to potential over-indebtedness among borrowers

## Why This Project
Most analysts in credit risk and portfolio management rely on Excel and reports spooled from core banking systems. It works — but it has limits. This project was built to demonstrate what becomes possible when domain knowledge meets a proper technical stack: automated calculations, dynamic dashboards, and outputs ready for credit committee presentation without manual intervention.

## Running the Project
1. Clone the repository
2. Create a `.env` file in the project root with your PostgreSQL credentials:
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=loan_portfolio
DB_USER=postgres
DB_PASSWORD=your_password_here
```
3. Install dependencies:
```bash
pip install psycopg2-binary pandas sqlalchemy matplotlib seaborn openpyxl python-dotenv faker
```
4. Create the database in PostgreSQL and run the SQL schema from `sql/portfolio_queries.sql`
5. Run the data generation script:
```bash
python data/generate_data.py
```
6. Open `notebooks/portfolio_analysis.ipynb` and run all cells
7. Open `dashboard/Loan_Portfolio_Dashboard.pbix` in Power BI Desktop

## Author
**Babatunde Atunbi** — Data Analytics | MIS, Portfolio & Risk Reporting | Financial Data Analysis
[LinkedIn](https://linkedin.com/in/atvnbi) | atunbitunde1@gmail.com
