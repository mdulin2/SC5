import requests
from hashlib import sha256

ip = "binary1.spokane-ctf.com"
port = "10001"

# Hash an arbitrary string for us
def hash_data(string):
	return sha256(string.encode('utf-8')).hexdigest()

def only_zeros(hash, amount):
	
	for i in range(amount):
		if(hash[i] != "0"):
			return False
	return True

def get_attempt():
	response = requests.get("http://{}:{}/question".format(ip,port)).json()
	return response

def send_attempt(req_id, nonce):	
	response = requests.get("http://{}:{}/answer?proof_id={}&nonce={}".format(ip,port,req_id,nonce))
	return response.json()

# Do over and over again until we find a nonce that works.
def calc_hash(data, diff):
	nonce = 1111
	hash = hash_data(str(nonce) + data)
	while(only_zeros(hash, diff) == False):
		nonce += 1
		hash = hash_data(str(nonce) + data)
	
	print(nonce)
	print(hash) 
	return nonce
		

proof_data = get_attempt()
difficulty = proof_data['difficulty']
data_to_prove = proof_data['data']
req_id = proof_data['proof_id']

# TODO - find hash here
nonce = calc_hash(data_to_prove, difficulty) 

print(send_attempt(req_id, nonce))

