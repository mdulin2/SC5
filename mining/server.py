from hashlib import sha256
import os,binascii
from flask import jsonify
from flask import Flask 
from flask import request
import uuid
import time


zeros = 7
flag = "SC5{adfasfdas}"

# Hash an arbitrary string for us
def hash_data(string):
	return sha256(string.encode('utf-8')).hexdigest()

# Ensure that the first X number of chars are zero
def only_zeros(hash, amount):
	
	for i in range(amount):
		if(hash[i] != "0"):
			return False
	return True
  
app = Flask(__name__) 
req_dict =  {}

@app.route("/question") 
def get_data():

	# Data we need hashed
	data = binascii.b2a_hex(os.urandom(200)).decode('utf-8')

	# Identifier for later
	proof_id = str(uuid.uuid4())

	req_dict[proof_id] = {"data" : data, "time" : int(time.time())}
	return jsonify({"data":data, "proof_id":proof_id, "difficulty" : zeros})

# Takes in two parameters - nonce and proof_id
@app.route("/answer")
def answer():
	# Find the attempt
	proof_id = request.args.get('proof_id')
	data = req_dict[proof_id]

	print('time:', int(time.time()), (data['time'] + 1))

	# Time check
	if(int(time.time()) > (data['time'] + 60)):
		return jsonify({"status" : "Timeout", "flag" : ""})

	nonce = str(request.args.get('nonce'))
	hash = hash_data(nonce + data['data'])
	proof_validity = only_zeros(hash, zeros)
	if(proof_validity == True):
		return jsonify({"status" : "Valid proof!", "flag" : flag})

	return jsonify({"status" : "Invalid proof", "flag" : ""})

if __name__ == "__main__": 
    app.run(debug=True) 
