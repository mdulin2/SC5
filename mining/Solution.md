## Solution 
- In the proof of work Bitcoin blockchain system, the 'work' is finding a hash with a sufficient amount of 0s at the front of it.
- This challenge is trying to emulate the bitcoin mining process. 
- To solve the challenge, write a script that prepends a nonce, checks the hash to have enough zeros over and over again until it's correct. 
- The networking of the client to get the information is taken care of.

