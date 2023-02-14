## Error Code Solution 

### Overview
- The purpose of this challenge is to turn an error message into usable code. 
- The code being executed looks like this: ``ls "xx" 2>&1 >/dev/null | <yy>``. 
    - The xx is the first input (which has a whitelist of characters) and yy must either be perl, python or php. 
- This challenge is loosely based upon this exploit by Orange Tsai: https://blog.orange.tw/2019/09/attacking-ssl-vpn-part-3-golden-pulse-secure-rce-chain.html


### What's Going on  
- First, the ls command is ran. Nothing out of the ordinary. This is given as input to the user.  
- Secondly,  ``2>&1 >/dev/null`` is ran. This is black magic bash scripting that takes the stderr (instead of the stdout) as the output. 
- Thirdly, this is piped (passed along) to one of the following programs: python, perl or php. 
- What happens when this is executed: 
    - ``ls: asfasfd: No such file or directory``
- How can we turn this into code? 


### Exploit 
- Can you think of anything that would allow for ``ls: something?`` in the code. To me, this looks like a *label* in traditionally assembly. 
- A label is used for jumps in assembly. However, these GOTO's are also supported in Perl land! 
- However, there is still the ``: No such file or directory`` at the end of this. In order to cancel that out, add a ``#``, which is a Perl comment, to comment out this part of the code. 
- We now that we can put this into Perl (because it supports labels.) How do we execute the code? 
Two answers: 
- One that needs the large amount of escaping... this is for the SECOND whitelist
   ./error_code '"system(\"ping google.com\"); #"' perl
- One that does not need any escaping, but has a harder whitelist (the second) 
  ./error_code "system 'cat flag' #" perl
