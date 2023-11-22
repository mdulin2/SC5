## Solution 
- The key is generated using a nonce in the range of 0,2**20, which is not very big. 
- Since this is a small number, an attacker can attempt **all** nonce within this space. By doing this, they can find the private key associated with the account.
- Write a script that attempts all keys within this range. Compare the 'address' from the output to the proper one. 
- Most of the code can be copied from the `gen.py` script in order to do this. 
- The nonce is '528493'. However, this isn't the flag. 
- The private key - flag - is L46nMXrYcZuVMo6i4fHuh4QdsLEokks1v98bW3N3ebVXcVsJzck4.
