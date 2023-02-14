
## How Does DSA Work? 
- Modular multiplicative inverse: 
	- a * x ≅ 1 (mod m)  
- Uses the security of the discrete log problem: 
	- https://www.doc.ic.ac.uk/~mrh/330tutor/ch06s02.html
	- https://medium.com/oxbridge-inspire/hard-problems-in-cryptography-cf0394cf8e79

## Steps for Key Generation
- 1: 
	- q: Select a prime. Half the size of p. 
- 2: 
	- p: Select a prime number. 
- 3: 
	- Select a generator alpha (h) which is the primitive root?
	- Unique cyclic group of the order q for all integers within p. 
	- To calculate this, do the following to calculate 'g': 
		- h = g^(p-1/q) % p
		- If h equals 1, then go back a step. 
		- If h does not equal 1, this is our 'g' value to use.
		- g=2 usually works
- 4: 
	- Select a random number 'd'. 
- 5: 
	- Compute the public key for signing
	- B = h^d mod p
- public key: 
	- p, q, h, B
- private key: 
	- d (random number) 
- Requirements: 
	- q divides (p-1)
	- 1 != g^((p-1)/q) % p = h 


## Signing & Verifying 
- Signing: 
	- Choose a random value 'k', where k is less than q-1. 
	- r = g^k % p % q
	- s = k^-1(m + dr) % q
	- Send 'm' (message), 'r' and 's'. 
- Verifying from m, r and s. 
	- x = s^(-1)*m % q
	- y = s^(-1)*r % q 
	- v = g^x*B^y % p % q 
- If 'v' == 'r', then the signature is valid. 

## Attacking
- Repeating 'r' values can decrypt the private key. 
	- Easy to detect, since the 'r' value will be the same between two signatures. 
- Revealing the 'r' value can decrypt the private key as well. 

## Resources 
- 'k' requirements: 
	- https://rdist.root.org/2010/11/19/dsa-requirements-for-random-k-value/
	- https://bitcoin.stackexchange.com/questions/35848/recovering-private-key-when-someone-uses-the-same-k-twice-in-ecdsa-signatures
	- https://github.com/tintinweb/ecdsa-private-key-recovery
	- https://blog.trailofbits.com/2020/06/11/ecdsa-handle-with-care/
- Recover key with known nonce: 
	- https://rdist.root.org/2009/05/17/the-debian-pgp-disaster-that-almost-was/