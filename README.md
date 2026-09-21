# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.

This is a number guessing game built with Streamlit. The app picks a secret number inside a range that depends on the difficulty you choose in the sidebar, and you try to find it before you run out of attempts. After every guess the game tells you whether to go higher or lower, keeps a running score, and ends when you either guess correctly or use up your attempts. The scoring rewards winning quickly, so a win on the first guess is worth more than a win on the sixth.

- [x] Detail which bugs you found.

| # | Where | Bug |
|---|-------|-----|
| 1 | `check_guess` | The hint messages were swapped. A guess that was too high returned "Go HIGHER!" and a guess that was too low returned "Go LOWER!", so the game pushed you away from the answer every time. |
| 2 | `check_guess` | A `try/except TypeError` branch compared the guess and the secret as text instead of numbers. In a string comparison `"9" > "42"` is True, because it compares character by character, so the direction was wrong even after the messages were swapped back. |
| 3 | `app.py` | The secret was converted with `str()` on every even numbered attempt, which is what triggered bug 2. |
| 4 | `update_score` | Off by one in the win payout. The formula was `100 - 10 * (attempt_number + 1)`, but `app.py` already counts the attempt before calling, so winning on the first guess paid 80 instead of 100. |
| 5 | `update_score` | A "Too High" guess on an even numbered attempt **added** 5 points instead of subtracting them, so guessing wrong could raise your score. |
| 6 | `app.py` | `st.session_state.attempts` started at 1 while the "New Game" button reset it to 0. A brand new game said "Attempts left: 7" and the off by one in the score came back even after bug 4 was fixed. |
| 7 | `tests/` | The three starter tests compared `check_guess(50, 50)` to the plain string `"Win"`, but the function returns an `(outcome, message)` tuple, so they failed on shape rather than on logic. |
| 8 | `tests/` | Running plain `pytest` failed at collection with `ModuleNotFoundError: No module named 'logic_utils'`. |

- [x] Explain what fixes you applied.

1. Moved `check_guess` and `update_score` out of `app.py` and into `logic_utils.py`, then updated the import in `app.py`. This is what made the logic testable without starting Streamlit.
2. Swapped the hint messages back so "Too High" tells the player to go LOWER and "Too Low" tells them to go HIGHER.
3. Deleted the string comparison fallback and cast both values with `int()` instead, which fixes the comparison no matter which type `app.py` passes in.
4. Changed the win formula to `100 - 10 * (attempt_number - 1)` and documented in the docstring that `attempt_number` is 1 based, so the off by one cannot quietly come back.
5. Made both wrong directions cost the same 5 points, which removed the even numbered bonus.
6. Changed the `attempts` initial value from 1 to 0 so it matches what the "New Game" button already did.
7. Updated the three starter tests to unpack the tuple and to check the hint direction, and added 8 new tests.
8. Added an empty `conftest.py` at the project root so plain `pytest` can find `logic_utils.py`.

## 📸 Demo Walkthrough

This walkthrough is a real game played on the fixed app with the secret set to 55 on Normal difficulty, so the numbers below are the actual values the app produced.

1. Start the app with `python -m streamlit run app.py`. The sidebar shows **Range: 1 to 100** and **Attempts allowed: 8**, and the main panel shows **"Attempts left: 8"**. Before the fix this said 7, because the attempt counter started at 1.
2. Open the **Developer Debug Info** expander to see the secret number, the attempt count, the score and the guess history. For this run the secret is **55**.
3. Enter a guess of **40** and click **Submit Guess**. The game replies **"📈 Go HIGHER!"**, which is correct because 40 is below 55. The score drops to **-5** and the attempt count goes to 1.
4. Enter a guess of **70**. The game replies **"📉 Go LOWER!"**, which is correct because 70 is above 55. The score drops to **-10** and the attempt count goes to 2. This is the guess that used to be broken twice over, once by the swapped message and once by the string comparison on the even numbered attempt.
5. Enter a guess of **55**. The game replies **"🎉 Correct!"**, shows balloons, and displays **"You won! The secret was 55. Final score: 70"**. The maths is `-5 - 5 + 80`, because a win on attempt 3 pays `100 - 10 * 2 = 80`.
6. The status is now `won`, so the app shows **"You already won. Start a new game to play again."** and stops accepting guesses.
7. Click **New Game** to reset the attempts, pick a fresh secret, and start over.

**Screenshot** *(optional)*: not included, the walkthrough above is the text record.

## 🧪 Test Results

```
$ python -m pytest tests/ -v

============================= test session starts ==============================
collecting ... collected 11 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  9%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 18%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 27%]
tests/test_game_logic.py::test_hint_direction_is_not_inverted PASSED     [ 36%]
tests/test_game_logic.py::test_string_secret_compares_numerically PASSED [ 45%]
tests/test_game_logic.py::test_win_on_first_attempt_pays_full_points PASSED [ 54%]
tests/test_game_logic.py::test_win_payout_drops_by_ten_per_attempt PASSED [ 63%]
tests/test_game_logic.py::test_win_payout_floors_at_ten PASSED           [ 72%]
tests/test_game_logic.py::test_too_high_on_even_attempt_loses_points PASSED [ 81%]
tests/test_game_logic.py::test_wrong_guess_penalty_is_symmetric PASSED   [ 90%]
tests/test_game_logic.py::test_wrong_guess_never_increases_score PASSED  [100%]

============================== 11 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
