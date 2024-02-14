import bip32utils
import random

address = "1PZE7KHa1Ujwd4jhUKNgUrjjtQeg7buSbM"
# Create the public key 
def generate_key(seed):
	bytes_seed = seed.to_bytes(32, 'big')
	key = bip32utils.BIP32Key.fromEntropy(bytes_seed)
	return key 

# Added function - mostly just a copy of generate_key
def de_generate(address):

	# Try every possible seed
	# Compare the address that we know to the address we have
	for i in range(0,2**20):
		bytes_seed = i.to_bytes(32, 'big')
		key = bip32utils.BIP32Key.fromEntropy(bytes_seed)
		if(address == key.Address()):
			print(key.WalletImportFormat())
			return i
		
print(address) 
print(de_generate(address))
