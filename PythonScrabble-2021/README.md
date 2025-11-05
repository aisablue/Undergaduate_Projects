# Scrabble (Text-Based Greek Version)

**Year:** 2021  
**Stage:** Undergraduate Coursework Project  
**Language:** Python  
**Original Code Comments:** Greek (kept intentionally to preserve authenticity)

This is a text-based implementation of **Scrabble in Greek**, where the human player competes against the computer.  
The game runs entirely in the terminal, without any graphical interface.  
The project focuses on **interaction design**, **data structures**, and **simple AI decision-making**, in the context of undergraduate coursework related to Human-Computer Interaction.

---

## Project Structure

The main program imports functionality from `classes.py`, which contains the core logic of the game.

### Key Utility Functions

| Function | Purpose |
|---------|---------|
| `value(word)` | Calculates the score of a word based on letter values. Used for both scoring and AI logic. |
| `freq(letter)` | Returns how many times each letter should appear in the main bag. |
| `accepted(w)` | Checks if `w` exists in the dictionary (`greek7.txt`). |
| `exist(w, lex)` | Checks if word `w` can be formed from the letters available in `lex`. |

---

## Class Overview

| Class | Description |
|------|-------------|
| `SakClass` | Represents the letter bag: adding, shuffling, drawing and restoring letters. |
| `Player` | Stores player letters and score, handles restoring and changing tiles. |
| `Human` | Inherits from `Player`. Requests input from user and validates played words. |
| `Computer` | Inherits from `Player`. Implements a **smart-fail** algorithm to simulate human-like decision making. |
| `Game` | Controls game setup, turn flow, scoring, termination, and menu handling. |

---

## AI Strategy: “Smart-Fail”

The computer does **not** always choose the highest-scoring word.  
Instead, it simulates **human decision behavior**, making the game more interesting:

1. Generate all possible combinations of letters.
2. Keep only valid dictionary words.
3. Score all words.
4. Sort them by score.
5. Choose based on probability:
   - **80%** chance: pick from the **higher-scoring** words
   - **20%** chance: pick from the **lower-scoring** words

This creates a more natural opponent — usually strong, but occasionally imperfect.

---

## Word Dictionary

The dictionary (`greek7.txt`) is implemented as a **Python dictionary** for speed.  
Dictionary lookups are **O(1)**, unlike lists which grow slower with size.

---

## Saving Game Statistics

Game statistics and scores are stored in **JSON** (`data.json`), because JSON:

- Is faster for small structured data
- Does not require binary serialization (unlike pickle)
- Is safer and human-readable

If `data.json` does not exist, it is **created automatically**.

---

## How to Run

Make sure the following files are in the *same folder*:

