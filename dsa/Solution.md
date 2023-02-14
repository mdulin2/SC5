## Solution 
### Challenge 1 - Explain DSA
- Ask for key points
- Qs: 
	- What is a cryptographic signature? Allow third parties to validate integrity of data without being able to alter it themselves. Asymmetric cryptography is amazing. 
	- What are the requirements for p and q?  
		- Both need to be prime numbers. 
		- q needs to be a factor of p - 1 
	- What type of number is g?
		- ?
	- What values are used for the public key? 
		- p, q, g, B
	- What values are used for verifying the signature? 
		- message, r, s
- Flag: finely voltage espresso

### Challenge 2 - Digitally sign data
- Digitally sign the message 501. 
- Values being used: 
	```
	p = 1031
	q = 103
	g = 320 
	secret (known as A) = 70 
	B = 48 
	k(nonce)  = 25
	message = 501
	```
- The signature consists of two new values: 
	- r and s. 
- Algorithm for r: 
	- r = g^k % p % q
	- 95 = (320^25) % 1031 % 103
- Algorithm for s: 
	- s = (k^-1) * (m + Ar) % q
	- s = (25^-1) * (501 + 70*95) % 103
		- (25^-1) is the modular multiplicative inverse. 
		- ``pow(25, -1, 103)`` is how you would implement this in Python3.
	- 10 = 33 * (501 + 70*95) % 103
- Full code for doing this can be found in ``dsa.py``
- Flag: 95, 10

### Challenge 3 - Hardness
- What difficult problem is the security of the algorithm based on? 
- Discrete log problem.
- X = g^s mod n
- Finding out s without having it is a difficult problem. 
- flag: Discrete log or Discrete logorithm

### Challenge 4 - Recovering the Private Key
- To recover the private key, we need to use the algorithm for generating 's' (s = (k^-1) * (m + Ar) % q) and move it around. 
	- The goal is to get 'A' on the side all by itself. 
- After moving this around, this looks like below: 
	- ``priv_key = ((s * k) - m) * r^-1 mod q``
- All we have to do is plug in these values from the previous attempt: 
	```
	p = 1031
	q = 103
	g = 320 
	B = 48 
	k(nonce)  = 25
	message = 501
	r = 95
	s = 57
	```
- Math setup: 
	- ``priv_key = ((s * k) - m) * r^-1 mod q``
	- ``priv_key = (((57 * 25) - 501) * 95^-1) mod 103``
		- 95^-1 is the modular multiplicative inverse. 
		- 90 = 95^-1
	- ``39 = (((57 * 25) - 501) * 90) mod 103``
- Flag: 39

### Challenge 5 - Recover k and the Private Key (Playstation 3) 
- The nonce is secret! However, given two signatures that use the same nonce, we can recover the nonce. 
- To do this, we need an algorithm that is capable of recovering that. 
- Once again ``s = (k^-1) * (m + Ar) % q``. If we have two signatures, we have s1 and s2 as well. 
- If we subtract s1 by s2, and redistribute, we end up with 
	- ``S1 – S2 = (k^-1) (message1 + A*r) - (k^-1) (message2 + A*r)``
- This simplifies to 
	- ``S1 – S2 = k-1 (message1 – message2)``
- If we redistribute for k, we get the following algorithm: 
	- ``k = ((s1 - s2)^-1 * (m1 - m2)) mod q``
- Plugging the numbers in: 
	- ```
	p = 1031
	q = 103
	g = 320 
	B = 48 
	sig1 = 500 (message), 75(r), 99(s) 
	sig2 = 501 (message), 75(r) 16(s) 
	```
	- k(nonce) = (99 - 16)^-1 * (500 - 501) mod 103
		- Multiplicative inverse of 83 ( from 99-16) is 36
	- 67 = 36 * (-1) mod 103
- 67 is the correct nonce! 
- Once we have the nonce, we can use the same algorithm as challenge 4 to recover the private key. 
	- We can choose either of the signatures to do this with now. 
- Plugging the numbers in: 
	- ``priv_key = ((s * k) - m) * r^-1 mod q``
	- ``priv_key = ((99 * 67) - 500) * 75^-1 mod 103``
		- Modular multiplicative inverse of '75^-1' is 11. 
	- ``101 = ((99 * 67) - 500) * 11 mod 103``
- Flag: 101


