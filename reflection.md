# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

The first time I ran the game, it looked perfect. However, once I started testing it, I noticed several bugs at once. To begin with, the button to start a new game wasn't working, and the clues the game was giving me were incorrect. Another bug I found was that even when I had one attempt left, the program would tell me I was “out of attempts” and give me the answer.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

For this project, I used the integrated vsCode Copilot tool. One of the suggestions the AI gave me was to correct the logic of the tracks because it was reversed. Although I read it multiple times, it wasn't until the AI clarified it for me that I fully understood. However, to correct the attempts, the first suggestion the AI gave me was wrong, but that was because my instructions on what needed to be fixed were not precise. However, after giving it all the context, it helped me fix the bug efficiently. 


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I verified that the bug was completely fixed by running the different test cases created by the AI and additionally manually testing each part of the application that was modified, to ensure that the fix would not affect any other area that was already fully functional. The AI was very efficient in creating each test case and additionally explaining to me what each one did to verify that I was not creating unnecessary test cases.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

Originally, the secret number in the application kept changing because Streamlit rebuilt the application every time the user interacted with it. Since this number was generated randomly without being saved, it caused the number to change every time the application was rebuilt. Therefore, it caused the number to change while the user continued playing. For someone who has never used Streamlit, the concept of “reruns” can be explained in different ways. To begin with, I can explain it as the app restarting from scratch each time. Due to this behavior, variables are not saved. I made several changes to ensure there is a stable secret number. However, the main change was that, together with the AI, I helped establish a state. This state helps us ensure that, regardless of whether the app rebuilds that number, it is saved.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

From what I learned in this project, I was able to develop several habits. To start this project, I changed the way I viewed AI for debugging. Although I was already familiar with and had used references before to help it learn about the project, I found it extremely interesting and efficient. For future projects, I know I will use AI to identify bugs more quickly, because as long as you identify them and explain them to the AI correctly, it is a much faster way to search than going line by line to discover what is not working.

