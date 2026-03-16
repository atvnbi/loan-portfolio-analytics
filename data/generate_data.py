import psycopg2
import random
from datetime import date, timedelta
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

fake = Faker()

# Database connection
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cur = conn.cursor()

# ── CONFIG ──────────────────────────
NUM_BORROWERS = 200
states = ["Lagos", "Abuja", "Kano", "Rivers", "Oyo", "Kaduna", "Enugu", "Delta"]
employers = ["Lagos State Government", "FCT Administration", "Rivers State Government",
             "Kano State Government", "Oyo State Government", "Federal Ministry of Finance",
             "Nigerian Army", "Nigerian Police Force", "NNPC", "CBN"]
loan_purposes = ["Personal", "Education", "Medical", "Home Improvement", "Business"]
employment_types = ["Civil Servant", "Military", "Paramilitary", "Federal Employee"]

# ── BORROWERS ───────────────────────
print("Inserting borrowers...")
borrower_ids = []
for _ in range(NUM_BORROWERS):
    monthly_salary = round(random.uniform(80000, 500000), 2)
    cur.execute("""
        INSERT INTO borrowers (full_name, employer, monthly_salary, state, employment_type, date_onboarded)
        VALUES (%s, %s, %s, %s, %s, %s) RETURNING borrower_id
    """, (
        fake.name(),
        random.choice(employers),
        monthly_salary,
        random.choice(states),
        random.choice(employment_types),
        fake.date_between(start_date=date(2022, 1, 1), end_date=date(2023, 12, 31))
    ))
    borrower_ids.append(cur.fetchone()[0])

# ── LOANS ───────────────────────────
print("Inserting loans...")
loan_ids = []
loan_data = []
for borrower_id in borrower_ids:
    loan_amount = round(random.uniform(100000, 5000000), 2)
    interest_rate = round(random.uniform(18, 36), 2)
    tenure_months = random.choice([6, 12, 18, 24])
    disbursement_date = fake.date_between(start_date=date(2023, 1, 1), end_date=date(2024, 6, 30))
    maturity_date = disbursement_date + timedelta(days=30 * tenure_months)
    monthly_repayment = round((loan_amount * (1 + interest_rate / 100)) / tenure_months, 2)
    loan_status = random.choices(
        ["Active", "Fully Paid", "Delinquent", "Written Off"],
        weights=[50, 25, 20, 5]
    )[0]
    cur.execute("""
        INSERT INTO loans (borrower_id, loan_amount, loan_purpose, interest_rate, tenure_months,
                           disbursement_date, maturity_date, monthly_repayment, loan_status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING loan_id
    """, (
        borrower_id, loan_amount, random.choice(loan_purposes), interest_rate,
        tenure_months, disbursement_date, maturity_date, monthly_repayment, loan_status
    ))
    loan_id = cur.fetchone()[0]
    loan_ids.append(loan_id)
    loan_data.append((loan_id, borrower_id, loan_amount, tenure_months,
                      disbursement_date, monthly_repayment, loan_status))

# ── REPAYMENTS ──────────────────────
print("Inserting repayments...")
for loan_id, borrower_id, loan_amount, tenure_months, disbursement_date, monthly_repayment, loan_status in loan_data:
    for month in range(1, tenure_months + 1):
        due_date = disbursement_date + timedelta(days=30 * month)
        if due_date > date.today():
            break
        if loan_status == "Fully Paid":
            payment_status = "Paid"
            actual_payment_date = due_date + timedelta(days=random.randint(0, 3))
            amount_paid = monthly_repayment
        elif loan_status == "Delinquent":
            payment_status = random.choices(["Paid", "Late", "Missed"], weights=[40, 35, 25])[0]
            actual_payment_date = due_date + timedelta(days=random.randint(5, 60)) if payment_status != "Missed" else None
            amount_paid = monthly_repayment if payment_status == "Paid" else (monthly_repayment * 0.5 if payment_status == "Late" else 0)
        elif loan_status == "Written Off":
            payment_status = random.choices(["Paid", "Missed"], weights=[20, 80])[0]
            actual_payment_date = due_date + timedelta(days=random.randint(1, 5)) if payment_status == "Paid" else None
            amount_paid = monthly_repayment if payment_status == "Paid" else 0
        else:
            payment_status = random.choices(["Paid", "Late", "Missed"], weights=[75, 15, 10])[0]
            actual_payment_date = due_date + timedelta(days=random.randint(0, 30)) if payment_status != "Missed" else None
            amount_paid = monthly_repayment if payment_status == "Paid" else (monthly_repayment * 0.7 if payment_status == "Late" else 0)

        cur.execute("""
            INSERT INTO repayments (loan_id, borrower_id, due_date, actual_payment_date,
                                    amount_due, amount_paid, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (loan_id, borrower_id, due_date, actual_payment_date,
              monthly_repayment, round(amount_paid, 2), payment_status))

# ── DPD CLASSIFICATIONS ─────────────
print("Inserting DPD classifications...")
today = date.today()
for loan_id, borrower_id, loan_amount, tenure_months, disbursement_date, monthly_repayment, loan_status in loan_data:
    outstanding_balance = round(random.uniform(0, loan_amount), 2)
    days_past_due = 0
    if loan_status == "Delinquent":
        days_past_due = random.randint(1, 90)
    elif loan_status == "Written Off":
        days_past_due = random.randint(91, 180)
    elif loan_status == "Active":
        days_past_due = random.choices([0, random.randint(1, 30)], weights=[85, 15])[0]

    if days_past_due == 0:
        dpd_bucket = "Current"
        classification = "Performing"
    elif days_past_due <= 30:
        dpd_bucket = "1-30 DPD"
        classification = "Watch"
    elif days_past_due <= 60:
        dpd_bucket = "31-60 DPD"
        classification = "Substandard"
    elif days_past_due <= 90:
        dpd_bucket = "61-90 DPD"
        classification = "Doubtful"
    else:
        dpd_bucket = "90+ DPD"
        classification = "Loss"

    cur.execute("""
        INSERT INTO dpd_classifications (loan_id, borrower_id, calculation_date,
                                         days_past_due, dpd_bucket, outstanding_balance, classification)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (loan_id, borrower_id, today, days_past_due, dpd_bucket, outstanding_balance, classification))

conn.commit()
cur.close()
conn.close()
print("All data inserted successfully!")