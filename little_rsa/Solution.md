## Challenge 0 
- The algorithm to encrypt a message is m^e mod N
- 453 = 101 ^ 3 mod 667
	- Python code: ``pow(101, 3, 667)``
- The reverse will decrypt it! 101 = 453 ^ 411 mod 667
	- ``pow(453, 411, 667)``
- Flag: 453

## Challenge 0.5 
- The algorithm to decrypt a message is c^d mod N, where 'c' is the ciphertext.
- 202 = 289 ^ 411 mod 667
	- Python code: ``pow(289, 411, 667))``
- Flag: 202

## Challenge 1 - Find 'd'
- 'd' is the modular multiplicative inverse of e % (p-1) * (q-1)
- So, ``d = e^-1 mod (157313963367733 - 1) * (205183854424553 - 1)``
- The following code can be calculate 'd' in Python3:
	- ``d = pow(e, -1, (p-1) * (q-1))``
- Flag: 19192493997001854947193454957


## Challenge 2 - Find 'm'
- Now that we have 'd', we can decrypt the message
- plaintext_message = (ciphertext ^ d) mod N
- 100658209704700468358422909 = (30062997357812254050845754858 ^ 19192493997001854947193454957) mod 32278285358594391272643148349
- Flag: 100658209704700468358422909

## Challenge 3 - Text of 'm'
- The original code uses 'int.from_bytes' with a big endianness to get the integer. We just need to convert it back. 
- The Python function ``int.to_bytes`` goes from integer to bytes. Two parameters need to be set: 
	- length: Anything bigger than 11 works.
	- endianness: big. This is known from the original code snippet given.
- ``recovered.to_bytes(11, 'big')`` will get the job done. 
- Flag: SC4{euler!}
