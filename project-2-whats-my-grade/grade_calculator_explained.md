# How the Grade Calculator Works (Plain English)

Think of the page as having three layers: **paint**, **skeleton**, and **brain**.

## 1. The Visual Style (`<style>`)

This is just the "paint and decoration" — colors, fonts, spacing. It gives the page a chalkboard-green background with cream text and a mono/typewriter font, like a gradebook.

None of this affects the math — it's purely how things look.

## 2. The Structure (`<body>`)

This lays out the boxes you see on screen:

- A title
- A line reminding you of the grading policy
- Four boxes — **Homework**, **Quizzes**, **Midterm**, **Final** — each with an input box for a score
- A big red "stamp" circle at the bottom that shows your final grade

For quizzes specifically, instead of one input box, there's a container (`quiz-rows`) that can hold *multiple* score boxes, plus a button to add more — because dropping the lowest 2 only makes sense if you have several quiz scores.

## 3. The Brain (`<script>`) — where the actual thinking happens

### `quizScores = [20]`
Just a list (array) storing whatever quiz scores you've entered. It starts with your one score, `20`.

### `renderQuizRows()`
Every time you add/remove a quiz, this function redraws the quiz input boxes so they match the current list. It also attaches a listener to each box: *"if the user types a new number here, update the list and recalculate."*

### `clamp(v)`
A small safety net. If you type something weird (blank, negative, over 100), it forces the number to stay between 0 and 100.

### `letterFor(pct)`
Takes your overall percentage and translates it into a letter grade (A, B+, C-, etc.) using standard cutoffs.

### `calculate()` — the heart of it
Every time any score changes, this function runs from scratch and does the following, category by category:

| Category | What happens |
|---|---|
| **Homework** | Score × 20% (0.20) → homework "points" |
| **Quizzes** | Sort scores low → high. If more than 2 scores, drop the lowest 2 and average the rest. If 2 or fewer, average whatever you gave it and show a warning note. Then multiply that average × 20% |
| **Midterm** | Score × 25% |
| **Final** | Score × 35% |

Then it **adds all four "points" together** → that's your overall grade. It updates the numbers on screen (the stamp, the math shown under each box, and the summary breakdown at the bottom).

### The last three lines
```js
[hwInput, midInput, finalInput].forEach(...)
renderQuizRows();
calculate();
```
These say: *"watch the homework/midterm/final boxes for changes, draw the quiz boxes, and run the calculation once immediately so the page isn't blank when it first loads."*

## Summary

| Layer | Role |
|---|---|
| CSS | The outfit — how it looks |
| HTML | The skeleton — boxes and buttons |
| JavaScript | The brain — reads your inputs, applies the weights and drop-lowest-2 rule, redraws results every time something changes |
