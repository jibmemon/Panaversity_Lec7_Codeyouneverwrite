# Prompt Record — Tour Payment Reconciliation App

**Date logged:** 2026-07-11

## Original Request

I want to make an application of book matching of people with me in tours.
Some are regularly paying and some have random payments. I am supposed to take Rs. 55,000/- from each member. Assume that I have a txt file in which I have added random entries of all the members and now I want to reconcile the payments — who has paid how much and who has not paid.

Do the following:

- First make me a txt file of random payments.
- Then make me an application that takes the txt file and sorts out my payments by book (member).
- We have the total amount in hand, but we need to reconcile it with the payments — who has paid and who has not — and we need to find some fake entries as well.

## Deliverables Produced

| File | Purpose |
|---|---|
| `payments.txt` | Sample randomized/shuffled payment log (15 members, mixed installments, overpayments, non-payers, planted fake entries) |
| `tour_reconciliation.html` | Standalone browser app: takes a roster + payments file, applies the Rs. 55,000/member rule, and outputs Settled / Overpaid / Pending / Not Paid status per member plus a separate "flagged for review" list |

## Key Rules Implemented

- Required amount per member: **Rs. 55,000** (editable in the app)
- Payment format: `Date, Name, Amount, TxnID`
- A member's total = sum of all their **valid** (non-flagged) entries
- Status logic:
  - `paid == 0` → **Not Paid**
  - `0 < paid < fee` → **Pending** (shows amount still owed)
  - `paid == fee` → **Settled**
  - `paid > fee` → **Overpaid** (shows excess)
- Fraud/anomaly checks (entries flagged and excluded from totals until manually reviewed):
  - Duplicate transaction ID reused across lines
  - Non-positive amount (zero/negative — e.g. stray refund-style entries)
  - Amount more than 2× the required fee (possible typo, e.g. extra zero)
  - Name that doesn't match anyone on the official roster

## Known Assumption / Limitation

- The member roster was invented for the demo (15 sample names) since the real roster wasn't provided — this needs to be swapped for the actual tour group member list.
- Fake-entry detection is rule-based (duplicate IDs, roster mismatch, outlier amount) — it flags likely problems for human review, it does not guarantee catching every disguised fake entry.

## Possible Next Steps (for chaining in a future session)

- Swap in the real member roster and real payment log
- Add export of the reconciliation results (e.g. to CSV or a printable report)
- Add a running "who to follow up with" reminder list for Pending/Not Paid members
- Add support for multiple tours/trips (separate ledgers) if this is recurring
