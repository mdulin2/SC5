## Challenge 

Since the early days of pwning computers with memory corruption issues (think of viewing/overwriting memory that the program should not control) several defense-in-depth security precautions have been added to modern operating systems. In general: what are these feartures, what do they do, how do they help security and how can they be defeated? 



### Nx/ DEP

- Questions:
  - What is the Nx bit for? What does DEP stand for? 
  - What type of attack does it prevent? 
  - What technique can be used to bypass the Nx bit? 
- Answers: 
  - Non-executable segment. In particular, used on heap and stack segments in order to make 'writable' segments not 'executable'. Segments can be issues as 'r', 'w' and 'x'. Segments that are 'w' will never be 'x'. Data execution prevention
  - This prevents people from writing code (in memory) then executing it. In particular, in this called 'shellcode'
  - Return oritented programming (ROP) 
- Further information: 
  - https://en.wikipedia.org/wiki/Executable_space_protection#Windows

### ASLR 

- Questions: 
  - What does ASLR stand for? 
  - What does it actually do? 
  - How is this helpful for security? 
  - What can be used in order to defeat ASLR? 
- Answers: 
  - Address Space Layout Randomization 
  - Randomly puts data segments (such as heap and stack) to random places in memory (not code segments though) 
  - Adds a sense of randomness to the attack. 
    - Makes the challenge either need brute-force or 
    - a memory leak of some kind in order to proceed with the exploit. 
    - In general, it just makes exploitation order. 
  - Brute force or a memory leak 
- Further information: 
  - https://en.wikipedia.org/wiki/Address_space_layout_randomization

### Stack Canaries 

- Questions: 
  - In general, what is a canary? 
  - What are stack canaries? 
  - Why are they useful? 
  - What can be used in order to defeat stack canaries? 
- Answers: 
  - Comes from a canary in the coal mine. Meant to tell the program that an usual event has occured 
  - Stack canaries are values (on the stack) that will crash the program if they are overwritten
  - These are useful because a basic buffer overflow (on the stack) will be caught by the program, making exploitation difficult to do 
  - Memory leak, brute force or overwriting a different section of memory besides the stack

### Bonus 

- What is PIE? How does it help with security? 
  - Portable independent executable. 
  - Randomizes the location of the code segment, making ROP or invoking other function very difficult. 
- What is the PLT or GOT table used for? What is RELRO? How does it help with security? 
  - Procedure LInkage Table and Global Offset Table. It helps with dynamic linking, of the program, to other built in libraries, such as libc. 
  - RELocation Read Only. Makes the several locations (in particular, the GOT) readable only and linked at linkage time. 
  - A common attack is to rewrite a GOT or PLT table entry to run your own malicious code. However, making this readonly prevents these types of attacks, 