"""
MONEY DETECTIVE
----------------
Scans a real transaction history CSV to find:
  1. Duplicate charges (same date + description + amount appearing more than once)
  2. Recurring / subscription-like charges (same description repeating across months)
  3. A verification check against a known baseline total

Expected CSV columns: Entry_ID, Date, Category, Description, Amount_PKR, Payment_Method
(A trailing "TOTAL" row, if present, is used as the baseline and excluded from analysis.)
"""

import csv
from collections import defaultdict
from datetime import datetime

FILE_PATH = "random_monthly_expenses_with_total_and_duplicates.csv"

def load_transactions(path):
    """Read the CSV, separate real transactions from the TOTAL summary row."""
    transactions = []
    known_total = None

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # The summary row has no Entry_ID/Date, and Category == 'TOTAL'
            if row["Category"].strip().upper() == "TOTAL":
                known_total = float(row["Amount_PKR"])
                continue
            if not row["Date"]:
                continue
            row["Amount_PKR"] = float(row["Amount_PKR"])
            row["Date"] = datetime.strptime(row["Date"], "%Y-%m-%d")
            transactions.append(row)

    return transactions, known_total


def find_exact_duplicates(transactions):
    """
    Flags transactions that share the same Date + Description + Amount.
    These are almost certainly double-charges / accidental repeats,
    since it's unlikely you'd pay the exact same amount for the exact
    same thing on the exact same day twice on purpose.
    """
    groups = defaultdict(list)
    for t in transactions:
        key = (t["Date"].date(), t["Description"].strip().lower(), t["Amount_PKR"])
        groups[key].append(t)

    duplicates = {k: v for k, v in groups.items() if len(v) > 1}
    return duplicates


def find_recurring_charges(transactions, min_occurrences=3):
    """
    Flags descriptions that repeat across multiple different months,
    often at similar amounts -- the signature of a subscription
    (internet, fiber, tuition, monthly fees) rather than a one-off cost.
    """
    by_description = defaultdict(list)
    for t in transactions:
        key = t["Description"].strip().lower()
        by_description[key].append(t)

    recurring = {}
    for desc, txs in by_description.items():
        months = {(t["Date"].year, t["Date"].month) for t in txs}
        if len(months) >= min_occurrences:
            amounts = [t["Amount_PKR"] for t in txs]
            recurring[desc] = {
                "count": len(txs),
                "months_seen": len(months),
                "amounts": amounts,
                "avg_amount": sum(amounts) / len(amounts),
                "category": txs[0]["Category"],
            }
    return recurring


def verify_against_known_total(transactions, known_total):
    """Sanity check: does summing every row match the baseline TOTAL row?"""
    calculated_total = sum(t["Amount_PKR"] for t in transactions)
    matches = abs(calculated_total - known_total) < 1  # allow float rounding
    return calculated_total, matches


def main():
    transactions, known_total = load_transactions(FILE_PATH)

    print("=" * 60)
    print("STEP 1: VERIFICATION AGAINST KNOWN BASELINE")
    print("=" * 60)
    calculated_total, matches = verify_against_known_total(transactions, known_total)
    print(f"Known baseline total (from file):     {known_total:,.0f} PKR")
    print(f"Sum of all individual transactions:   {calculated_total:,.0f} PKR")
    print(f"Match: {'YES ✅' if matches else 'NO ❌ -- investigate before trusting results below'}")
    print(f"Total transactions counted: {len(transactions)}")

    print("\n" + "=" * 60)
    print("STEP 2: EXACT DUPLICATE CHARGES")
    print("=" * 60)
    duplicates = find_exact_duplicates(transactions)
    if not duplicates:
        print("No exact duplicates found.")
    else:
        total_duplicate_waste = 0
        for (date, desc, amount), txs in sorted(duplicates.items()):
            extra_charges = len(txs) - 1  # first one is legitimate, rest are extras
            waste = extra_charges * amount
            total_duplicate_waste += waste
            print(f"- {date} | {desc.title()} | {amount:,.0f} PKR charged {len(txs)} times "
                  f"(Entry IDs: {[t['Entry_ID'] for t in txs]})")
        print(f"\nPotential money lost to duplicate charges: {total_duplicate_waste:,.0f} PKR")

    print("\n" + "=" * 60)
    print("STEP 3: RECURRING / SUBSCRIPTION-LIKE CHARGES")
    print("=" * 60)
    recurring = find_recurring_charges(transactions, min_occurrences=3)
    if not recurring:
        print("No recurring charges found across 3+ months.")
    else:
        for desc, info in sorted(recurring.items(), key=lambda x: -x[1]["count"]):
            print(f"- {desc.title()} ({info['category']}): seen in {info['months_seen']} different months, "
                  f"avg {info['avg_amount']:,.0f} PKR/charge, total {sum(info['amounts']):,.0f} PKR")

    print("\nDone. Review the flags above -- anything you don't recognize is worth double-checking.")


if __name__ == "__main__":
    main()
