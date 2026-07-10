# Project 2 — What's My Grade, Really

## The Problem
Generic "grade calculator" apps don't know a specific teacher's actual rules —
weighted categories, dropped lowest scores, or special replacement policies.
This project encodes the exact rules from my teacher's syllabus and my real
scores to find my true current grade, and what I need on the final exam to
hit a target.

## AI Tool Used
Claude (Anthropic)

## Data Used
`grades_and_rules.txt` — my scores and the teacher's grading policy:
- Homework: 20%
- Quizzes: 20% (lowest 2 scores dropped)
- Midterm: 25%
- Final Exam: 35%

*(Note: sample/practice data used here. A real submission should use the
student's actual scores and their own teacher's real policy.)*

## Verification Against a Known Fact
Before running the script, I hand-calculated the quiz category myself:
- Quiz scores (out of 20): 18, 15, 20, 12, 17, 19, 14, 16
- Dropping the lowest 2 (12 and 14) leaves: 15, 16, 17, 18, 19, 20
- Average = 105 / 6 = 17.5 out of 20 = **87.5%**

The script's output matched this exactly (87.50%), which confirmed I could
trust the rest of the calculation (homework average, midterm weighting, and
the final-exam-needed calculation).

## What the Script Found
- Homework average: 88.90%
- Quiz average (lowest 2 dropped): 87.50%
- Midterm: 84%
- Current weighted grade (before final): 56.28 out of 65 possible points
- **To reach a target overall grade of 90%, a final exam score of 96.34% is needed**

## What Worked / What Didn't
- The drop-lowest-N logic worked correctly on the first attempt by sorting
  scores and slicing off the lowest N before averaging.
- Converting quiz scores (out of 20) to a percentage before applying the
  category weight was an easy step to originally forget — worth double
  checking against the syllabus units (some categories may already be
  entered as percentages, others as raw points).
- The script also correctly warns if a target is mathematically impossible
  (needed final > 100%) or already guaranteed (needed final < 0%), which is
  a useful edge case to have caught early.

## Final Result
A concrete, motivating number: **96.34% needed on the final exam** to reach a
90% overall grade — tells me exactly how hard I need to study and whether the
target is realistic.

## How to Re-run
```
python script.py
```
(Edit the score lists and weights directly in the script, or adapt it to read
from a file, as new scores come in throughout the term.)
