# Prompts Used — Project 2: What's My Grade, Really

## Initial Prompt
"Here are my scores: [pasted homework, quiz, and midterm scores]. Here is my
teacher's actual grading policy: Homework 20%, Quizzes 20% (lowest 2 dropped),
Midterm 25%, Final 35%. Write a script that calculates my current overall
grade, applying all these rules correctly, and shows the math per category."

## Follow-up Prompt (verification)
"I calculated the quiz category by hand: dropping the lowest 2 scores (12 and
14) and averaging the rest gives 87.5%. Does your script's quiz average match
this exactly?"
→ Confirmed: script output matched exactly (87.50%).

## Follow-up Prompt (target grade)
"What score do I need on the final exam to reach an overall grade of 90%?"
→ Response: 96.34% needed on the final exam.

## Follow-up Prompt (edge cases)
"What should the script do if the needed final score is above 100% or below
0%?"
→ Added handling to print a warning if the target is unachievable, or confirm
if the grade is already secured regardless of the final.
