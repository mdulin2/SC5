## Challenges 

### Challenge 1 - Explain DSA
- Manually verify. Students need to go up to coaches and ask about this. 
- Ask for key points
- Qs: 
	- What is a cryptographic signature? 
	- What are the requirements for p and q?  
	- What type of number is g?
	- What values are used for the public key? 
	- What values are used for verifying the signature? 

### Challenge 2 - Digitally sign data
- Given a message, sign this data. The key information is as follows: 
	```
	p = 1031
	q = 103
	g = 320 
	secret (known as A) = 70 
	B = 48 
	k(nonce)  = 25
	message = 501
	```
- Ask for the tuple in a specific format. 
- Since code needs to be written, give them a few hints...:
	- When you see k^-1, this doesn't mean 1/k. This means the modular multiplication inverse. 
		- Code for this in newer versions of Python3
		- ``pow(number, -1, modular_field)``
	- Signing: 
		- r = g^k % p % q
		- s = k^-1(m + dr) % q
		- Send 'm' (message), 'r' and 's' as the public key. 
	- Verifying from m, r and s. 
		- x = s^(-1)*m % q
		- y = s^(-1)*r % q 
		- v = g^x*B^y % p % q 
	- 'v == s' means the verification was done correctly. 

### Challenge 3 - Hardness
- What difficult problem is the security of the algorithm based on? 
- Hint: Diffie Hellman and El Gamel use the same hard problem.

### Challenge 4 - Recovering the Private Key
- Once the nonce of a signature is known, the private key (A or d) can be recovered. Recover the private key from the following public key and signature: 
	```
	p = 1031
	q = 103
	g = 320 
	B = 48 
	k(nonce)  = 25
	message = 501
	r = 95
	s = 57
	Notice... there is NO 'A or d' here! This is what we want to recover!
	```
- Hint: 
	- ``x = ((s * k) – m * r^-1 mod q``
	- https://rdist.root.org/2009/05/17/the-debian-pgp-disaster-that-almost-was/

### Challenge 5 - Recover k and the Private Key (Playstation 3) 
- Ever wonder what real hacks are made of? The group Fail0verflow recovered the playstation 3 game signing key because of poor key management. 
- What did they do? They reused nonce values between signatures! That's all it takes to mess up cryptography. Below, are two signatures. From this, recover the nonce and then (as with challenge 4) the private key. 
```
p = 1031
q = 103
g = 320 
B = 48 
sig1 = 500 (message), 75(r), 99(s) 
sig2 = 501 (message), 75(r) 16(s) 
```
- Hints: 
	- Remember that this works in a modular field. 
	- Remember the multplicative inverse.
	- https://rdist.root.org/2010/11/19/dsa-requirements-for-random-k-value/
