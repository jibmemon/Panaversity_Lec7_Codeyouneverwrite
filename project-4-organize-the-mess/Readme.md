# Code You Never Write — Final Report

**Name:** Syed Abdullah Ali
**AI Tool(s) Used:** Claude (Anthropic)

---

## Project 1 — Money Detective

**Problem:** Instead of tracking spending going forward, this project hunts
for leaks hiding in past transaction history — recurring charges, forgotten
subscriptions, and duplicate/accidental charges.

**Initial Prompt:** "Here is my transaction history in CSV format: [pasted
data]. Write a Python script that: (1) finds recurring charges that repeat
weekly or monthly, (2) flags possible forgotten subscriptions, (3) flags
duplicate or repeated payments (same amount, same/similar description,
within a few days). Also have it print the total spend for each month."

**Improved Prompts:**
- Asked it to fix a display bug (a stray negative sign in the duplicate
  charge output).
- Asked it to explain its logic in plain English.

**Verification:** Hand-calculated the true monthly totals beforehand
($1,724.94 for November, $1,735.10 for December). The script's output
matched both exactly, confirming the rest of its logic could be trusted.

**What Worked / What Didn't:** Recurring-charge detection worked well once
amounts were compared with rounding instead of exact equality. The
duplicate-detection output had a small display bug (negative sign) on the
first run, fixed with `abs()`.

**Final Result:** Found a duplicate $22.30 charge on the same day (a likely
accidental double-charge) and flagged 5 recurring subscriptions worth
reviewing.

---

## Project 2 — What's My Grade, Really

**Problem:** Generic grade calculators don't know a specific teacher's exact
rules — weighted categories, dropped lowest scores, replacement policies.
This project encodes those exact rules to find the true current grade.

**Initial Prompt:** "Here are my scores: [pasted]. Here is my teacher's
actual grading policy: Homework 20%, Quizzes 20% (lowest 2 dropped), Midterm
25%, Final 35%. Write a script that calculates my current overall grade,
applying all these rules correctly, and shows the math per category."

**Improved Prompts:**
- Asked what final exam score is needed to reach a 90% target grade.
- Asked it to handle edge cases (target impossible or already secured).

**Verification:** Hand-calculated the quiz category myself — dropping the
lowest 2 scores and averaging the rest gave 87.5%. The script's output
matched exactly, confirming the category weighting and drop-lowest logic
were correct.

**What Worked / What Didn't:** The drop-lowest-N logic worked correctly
immediately. Converting quiz scores (out of 20) to a percentage before
weighting was an easy step to originally overlook.

**Final Result:** A final exam score of 96.34% is needed to reach a 90%
overall grade — a concrete, motivating number.

---

## Project 3 — The Books Don't Match

**Problem:** Reconciling a known, hand-counted total (money collected for a
group trip) against a messy digital payment record with inconsistent
formatting, to find exactly what's missing and who still owes money.

**Initial Prompt:** "My known correct total is $600, collected from 12
people at $50 each. Here is the raw payment record exactly as exported:
[pasted]. Here are my rules for interpreting the names/handles: [pasted].
Write a script that reconciles these, finds the gap between $600 and what's
actually recorded, and lists exactly which people/amounts are unaccounted
for."

**Improved Prompts:**
- Asked it to confirm the exact size of the gap and name the missing payer.
- Asked how it would handle someone paying in multiple smaller installments.

**Verification:** Stated the known total ($600) up front as the target the
reconciled record needed to match.

**What Worked / What Didn't:** Applying interpretation rules as a simple
lookup (messy label → real name) resolved all ambiguous entries in one pass.
It mattered to give the AI the raw record exactly as exported, without
cleaning it up first, so the real inconsistencies could be handled properly.

**Final Result:** The entire $50 gap was explained by one person (missing
from the record) who had not yet paid — no need to re-check the other 11
payments, which all reconciled exactly.

---

## Project 4 — Organize the Mess

**Problem:** Digital clutter (duplicate files, forgotten downloads, oversized
files) builds up over time. This project finds and organizes it safely,
without risking damage to real files.

**Initial Prompt:** "I have a messy folder. Write a Python script that: (1)
finds duplicate files based on file content, (2) flags files over 500KB,
(3) groups files by type. Before doing anything, the script must run in a
safe 'dry run' mode by default that only prints the full plan and must NOT
touch, move, rename, or delete anything unless I explicitly pass an
--execute flag."

**Improved Prompts:**
- Asked it to confirm the plan was shown in full before anything ran.
- Asked it to write results into a new folder rather than modifying
  originals.
- Asked for confirmation that the original folder was unchanged after
  execution.

**Verification:** Followed the required safety order exactly: made a full
backup of the folder before running anything, reviewed the complete dry-run
plan, and only then approved execution. Afterward, manually confirmed all
original files were still present, unchanged, in the source folder.

**What Worked / What Didn't:** Hashing file *contents* (not just filenames)
correctly caught duplicates that had different names but identical content.
The dry-run/execute split made it safe by default — the script's normal
behavior is always the read-only preview.

**Final Result:** Found 3 sets of duplicate files and one oversized file
worth reviewing, all confirmed safe — the original folder was untouched
throughout the entire process.

---

## Overall Reflection
The consistent thread across all four projects was the verification step:
in each case, a fact was established *before* looking at the AI's output —
a known total, a hand-calculated category average, a known file count — and
the AI's result was only trusted once it matched that fact exactly. This
made it possible to act as a client describing the problem clearly, rather
than someone reading and debugging the code line by line.
