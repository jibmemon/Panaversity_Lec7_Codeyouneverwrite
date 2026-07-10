# Money Detective — Reusable Prompts

## 1. Initial Prompt (To Build the Script)

```
I want to find spending leaks in my own real transaction history — not build a
forward-looking budget, just analyze what already happened.

I'm attaching/pasting a CSV of my real transactions. It has these columns:
Entry_ID, Date, Category, Description, Amount_PKR, Payment_Method. There is also
a TOTAL row at the bottom with my known baseline total spend.

Please write a Python script that:
1. Loads the CSV and separates the TOTAL row from the real transactions
2. Finds exact duplicate charges — same date, same description, and same amount
   appearing more than once (likely double-billing)
3. Finds recurring/subscription-like charges — the same description repeating
   across 3 or more different months
4. Verifies the sum of all transactions against the known TOTAL row, so I can
   confirm the script is reading the data correctly
5. Prints a clear, readable summary of the findings

After the script runs, explain in plain English what the code is actually doing,
step by step, so I understand the logic and don't just trust it blindly.
```

---

## 2. Fix-It Prompt (Use if Something Breaks or Looks Wrong)

```
The script threw an error / gave a result that doesn't match my known total.
Here's what happened:


"the calculated total was 1,450,000 but my real total is 1,487,638"

It was missing some enteries that had no descrition.
So I asked to also read them count them also.


Please:
1. Figure out exactly why the mismatch/error is happening
2. Fix the script so it handles this correctly
3. Re-verify the total against my known baseline after the fix
4. Tell me in plain English what was wrong and what you changed
```
---

### Notes

- **When to use Prompt 1:** every time you start fresh with a new dataset or want to rebuild the script from scratch.
- **When to use Prompt 2:** if the script errors out, or the calculated total doesn't match your known baseline — common causes include different date formats, currency symbols in the amount column, extra/missing columns, or blank rows.
