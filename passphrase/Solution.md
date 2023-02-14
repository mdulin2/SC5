## Overview
- The main purpose of this is to learn about cryptographic passphrases for key recovery. By having the passphrase, it is possible to get the key back! https://www.thecryptomerchant.com/blogs/resources/hardware-wallet-recovery-seeds-explained

## Solution
- The students are given the encode file, word list and passphrase (but not the decoder). 
- This gets the students to figure out *what* a recovery passphrase actually is and *how* it is used in the real normal (particularly, with cryptocurrency).
- The goal is to get the students to write their on decoder to see what the key is. 
- The decoder (with a simple coding version in decode.py) is a 32 bit value mapped to a word in the word list.
	1. For each word (left to right) replace the word with the index (0 based) from the word list.
	2. For each index of the word (again, left to right) put this to the power of the base (32). 
		- For example, the 3rd word in the passphrase with being the index of bacon(1) would look like the following: 
		- 2 * 32 ** (3-1). 
	3. Add these together to get back the key.
	4. Convert from decimal (or hex) to base32. 
- The decimal solution is `1043914648681`. 
- The base 32 solution (actual solution) is UC72IR39.
	


### Key Generation
Code to generate the key 
```print encode(9 * 32 ** 0 + 3 * 32 ** 1 + 27 * 32 ** 2 + 18 * 32 ** 3 + 2 * 32 ** 4 + 7 * 32 ** 5 + 12 * 32 ** 6 + 30 * 32 ** 7)```
