# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

When I first ran the game, it looked normal with a place to enter our guess, a button to submit those guesses, restart a game and a check box to indicate whether we want to show hints or not. But I noticed that several parts were not working properly.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

1. The attempt counter was faulty because my first guess was not counted, so the total number of attempts was inaccurate. 
2. The “New Game” button also did not properly reset the game, and I had to reload the page to start over. 
3. I also noticed that the hints were backwards, i.e, when it should say go Lower, it says go higher and vice versa.
4. The final score was calculated incorrectly.
5. The secret number could sometimes be outside the range for the selected difficulty.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
|60 | Go LOWER! | Go HIGHER| None |
| 40| Go LOWER!| Go HIGHER!| None|
| 10 | Go HIGHER!| Go LOWER!| None|

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude Code inside VS Code. I fixed one bug at a time instead of asking it to fix everything at once, so I could check each change before moving on to the next one. I also made it run the tests and start the game in front of me, so I could see the results myself instead of just believing what it told me.

**An AI suggestion that was correct**

I found the two broken functions myself. Playing the game showed me the hints were backwards and the score was wrong, so I read through `app.py` and worked out that `check_guess` and `update_score` were the ones causing it. The backwards hints were easy to spot, because the too high branch said "Go HIGHER!" and the too low branch said "Go LOWER!".

What I did ask Claude about was a piece of code inside `check_guess` that I did not understand. It explained that when the secret is stored as text instead of a number, Python compares them letter by letter, so `"9"` looks bigger than `"42"`. It also pointed out that `app.py` was turning the secret into text on every second guess, which is what set that off. Both of those were correct.

I checked it in two ways. I wrote a test for it, and the test failed on the old code and passed on the new code. Then I played the game and guessed 60 when the secret was 50, and it correctly told me to go lower.

**An AI suggestion that was incorrect or misleading**

I asked Claude to write tests for the scoring bug and it gave me six, and all six passed. That looked good, but I asked it to run those same tests against the old broken code to prove they were doing their job. One of them passed there too, which meant it was not really checking anything. It only tested that a win very late in the game is worth 10 points, and both the old and new versions give 10 points that late, so that test could never fail.

I checked this by saving a copy of the old function and running each test against it one by one. The fix was to test an earlier guess instead, where the old code gives 10 points and the new code gives 20. That version does fail on the old code, which is how I knew it was working. What I learned is that a test passing does not mean the test is any good.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I did not count a bug as fixed until the test failed before the change and passed after it. I ran every new test against the old broken code first, to make sure the test actually noticed the bug. After that I ran all the tests together, and then I opened the real game and played it, because the tests only check the small functions and not whether the app is using them properly.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

There are now 11 tests and they all pass. The most useful one checks that winning on the first guess gives 100 points. It failed on the old code with 80, because the old formula counted the attempt twice.

I also ran into two problems with the tests themselves. Running `pytest` gave an error saying it could not find `logic_utils`, which I fixed by adding an empty `conftest.py` file in the main folder. The three starter tests were also failing for a reason that had nothing to do with the game, because they expected `check_guess` to return just `"Win"` when it actually returns the result and the hint message together. I updated them to read both.

The most important thing happened after all the tests were passing. I played the game and winning on the first guess still gave 90 points instead of 100, and a brand new game said "Attempts left: 7". The scoring function was fine. The real problem was that `app.py` started the attempt counter at 1 while the New Game button set it back to 0, so the two did not match. No test on the scoring function could ever have caught that. I changed the starting value to 0 and after that the first guess win gave 100.

- Did AI help you design or understand any tests? How?

Yes. Claude wrote the first versions of the scoring tests and explained why the `conftest.py` file was needed. It also helped me see the difference between a test that just agrees with whatever the code does and a test that would actually catch the bug if it came back. To play the game automatically it used a Streamlit tool called `AppTest`, which runs the app from code, so I could replay a whole game without clicking through the browser every time.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type in a box, Streamlit runs your whole Python file again from the top. That means a normal variable is useless for anything you want to keep, because `secret = random.randint(1, 100)` would pick a new number on every click and you could never win. `st.session_state` solves this by storing values outside the script so they survive the reruns, and the `if "secret" not in st.session_state` guard makes sure the value is only set the first time.

The lesson I took from it is that state bugs are easy to miss. My attempt counter started at 1 instead of 0, and because that line only runs once, my scoring function was correct and all my tests passed while the game still gave the wrong score.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?

The habit I want to keep is fixing one thing at a time and checking it before moving on. I did not ask the AI to fix the whole game in one go. I played the game first and read through `app.py` until I could point at the two functions causing the problems. Then I moved `check_guess` on its own and fixed the hints, and played the game to see them come out right. Then I did `update_score` as a separate step, then the tests, then I ran `pytest`, then I opened the app again.

Doing it in that order is what caught the bugs. Because I already knew the first fix worked, I knew that anything that broke afterwards came from the change I had just made.

- What is one thing you would do differently next time you work with AI on a coding task?

I would open the actual game much earlier instead of treating passing tests as the finish line. All of my tests were passing while the game was still giving the wrong score, because the real problem had moved into `app.py` where none of my tests were looking. Next time I will switch between testing and playing rather than doing all the testing first and the playing at the end.

I would also question the AI sooner. A few times it told me something was done when really only part of it was done. Asking it to show me the output works much better than asking it whether something is fixed.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I used to read AI code and check whether it looked sensible, and this project showed me that looking sensible is exactly the problem, because the broken code was clean and easy to read and still completely wrong. Now I treat AI code as a first draft written by someone who never ran it, and I only believe it once I have seen it fail before the fix and pass after it.

**A suggestion I rejected**

At one point the AI suggested leaving `check_guess` as it was and changing the three starter tests to expect the backwards hints instead. That would have made everything pass while the game stayed broken. I said no, because tests are supposed to describe what the game should do, not be rewritten to agree with a bug. I fixed the messages inside the function instead, and then updated the tests to match.
