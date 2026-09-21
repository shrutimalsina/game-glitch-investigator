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
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
