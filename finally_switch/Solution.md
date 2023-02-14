## Finally Switch 

### Overview
Python 2 is DEPRECATED. Commonly, deprecated software has terrible security  
flaws in it. When software with known flaws is used, it is just looking to  
be exploited :) 

### Exploit
In Python2 there are two ways to get user input: 
- input 
- raw_input

For some weird reason, only `raw_input` defaults accepts strings.   
Instead, `input` accepts literaly python code... but, why!?   
For some reason, `input` acts as ``eval(<user_input>)``, which literally
executes Python code! This is purposeful command injection that **IS NOT  
WELL KNOWN**. Ugh, terribly for security...  
  
  
To actually exploit this, just run some Python code :)   
The program imports 'os', which is not necessary, but easier.   
- ``system('/bin/sh)`` or ``system('cat flag.txt')`` <-- answer

To make this more interesting, it is possible to complete this challenge  
without needing us to import the 'os' package! We just need to import  
this with INLINE imports (only trick): 
- ``__import__("os").system("/bin/sh")`` 
  
A good explanation for this can be found at https://medium.com/@abdelazimmohmmed/python-input-vulnerability-30b0bfea22c9

