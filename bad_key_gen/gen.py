import bip32utils
import random

# Create the public key 
def generate_key(seed):
	bytes_seed = seed.to_bytes(32, 'big')
	key = bip32utils.BIP32Key.fromEntropy(bytes_seed)
	return key 
	
seed = random.randint(0, 2 ** 20) 
print(seed) 
key = generate_key(seed) 
address = key.Address()
print(address) 
