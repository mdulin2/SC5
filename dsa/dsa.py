
def sign(large_prime, small_prime, generator, random_k, B, priv_key_d, message):
	r = ((generator**random_k) % large_prime) % small_prime

	k_inverse = pow(random_k, -1, small_prime)
	s = (k_inverse * (message + priv_key_d * r)) % small_prime

	return message, r, s

# Verify the signature...
def verify(message, r, s, q, g, B, p):
	x = (pow(s, -1, q) * message) % q

	y = (pow(s, -1, q) * r) % q

	v = ((g**x * B**y) % p) % q
	return v

'''
Trying similar to this: https://bitcoin.stackexchange.com/questions/35848/recovering-private-key-when-someone-uses-the-same-k-twice-in-ecdsa-signatures]
Trail of Bits paper forgets to mention the modulus...

Algorithm:
k = ((s1 - s2)^-1 * (m1 - m2)) mod q

Can get to this by starting with the values used to calculate s1 and s2. 
Then, subtract s1 from s2 and redistribute to get k on the one side only. 
'''
def recover_k(s1, s2, message1, message2, q):

	# Reuse of 'k' value makes it possible to recalculate it. 
	s_inverse = pow((s1 - s2), -1, q)
	return ((message1 - message2) * s_inverse) % q

'''
By knowing the nonce, we can get the private key. 
private_key = ((s * k) - H(m)) * r^-1 mod q
'''
def recover_priv_key(s, k, message, r, q): 
	tmp_var = ((s * k) - message) * pow(r, -1, q)
	key = tmp_var % q 
	return key

# 95, 10 
def challenge2():
	message, r, s = sign(1031, 103, 320, 25, 48, 70, 501)
	print(r,s)

# 39 
def challenge4(): 
	print(recover_priv_key(57, 25, 501, 95, 103))


# 101
def challenge5(): 
	# Recover the nonce first 
	k = recover_k(99, 16, 500, 501, 103) 

	# After recovering the nonce, calculate the private key.
	print(recover_priv_key(99, k, 500, 75, 103))


def test_setup(): 
	message, r, s = sign(1031, 103, 320, 25, 48, 70, 501)
	v = verify(501, r, s, 103, 320, 48, 1031)
	print(v, r, v==r)