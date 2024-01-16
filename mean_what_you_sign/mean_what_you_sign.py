import Crypto.PublicKey.RSA as RSA
from Crypto import Random
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
import base64


public_key=None
private_key=None

# Cryptographic operations
# Apparently, this uses textbook RSA?
# https://stackoverflow.com/questions/4232389/signing-and-verifying-data-using-pycrypto-rsa
def gen_keys():
    global public_key, private_key
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    private, public = key, key.publickey()
    return public, private

def sign_data(data_to_sign):

    # Object that performs the signing
    signer = PKCS1_v1_5.new(private_key) 
    digest = SHA.new()

    # Hash the data being signed
    digest.update(data_to_sign.encode("utf-8")) 

    # Sign the data and return the signature
    return signer.sign(digest) 

def initialize_crypto():
    global public_key
    global private_key
    public_key, private_key = gen_keys()
    

# List of users
user_lst = []

# Users session data
user_data = {}

# The current users name
active_user = None


def interactive():
    options = '''
My Signing Handler
======================
1. Login
2. Create User
3. Identify self
4. View session data
5. Load old session
6. Exit
>'''
    print(options) 

    input_option = -1 

    # Handle a set of options
    while(input_option != int and (input_option > 10 or input_option < 1)):
        input_option = int(input()) 
        
    return input_option        

# Login as a particular user
def login():
    global user_lst
    global active_user
    global user_data

    new_user = input("User:") 
    if(new_user.lower() == 'admin'):
        print("Nice try ;)")
        return False

    elif(new_user in user_lst):
        active_user = new_user

        random_data = input("Random Data:")

        # Add session data
        user_data[new_user] = sign(new_user, random_data)

        return True
    else: 
        print("User DNE!") 
        return False

# Sign the auth object for the user
def sign(username, random_nonce):
    '''
    Data to sign 
    - Username | Session random data
    '''
    
    return sign_data(username + random_nonce)

# Create user - don't allow them to create the admin user
def create_user():
    global user_lst
    global active_user

    new_user = input("New user:") 
    if(new_user.lower() == 'admin'):
        print("Nice try ;)")
        return False

    user_lst.append(new_user) 
    return True

# Use user provided object as signature, username and session nonce
def take_old_signature():
    global active_user 
    global user_data

    old_username = input("Username: ") 
    old_random_value = input("Random Data: ") 
    old_signature = input("Old Signature: ").encode("utf-8") 

    # Calculate the signature and compare it against the one provided
    new_sig = sign(old_username, old_random_value) 
    new_sig_base64 = base64.b64encode(new_sig)

    #print(new_sig_base64.decode("utf-8"), old_signature.decode("utf-8"), old_username) 
    if(new_sig_base64 == old_signature):
        print("Logged in!") 
        active_user = old_username
        user_data[old_username] = old_username
        return True
    else:
        print("Login failed :(") 
        return False

def get_session_data():
    global active_user 

    return base64.b64encode(user_data[active_user])

def read_flag(): 
    file = open("flag.txt", "r")
    content = file.read()
    file.close()
    return content

def loop():

    go = True
    while(go):
        d = interactive() 
        if(d == 1):
            login()
        elif(d == 2):
            create_user()
        elif(d == 3):
            print("Hello, my name is {}".format(active_user))
        elif(d == 4):
            session = get_session_data()
            print(session.decode('utf-8'))

        elif(d == 5):
            take_old_signature()
        elif(d == 6):
            go = False

        # Shows flag and exits if you won :) 
        if(active_user == 'Admin' or active_user == 'admin'):
            flag = read_flag()
            print("-------------------------------")
            print(flag)
            print("-------------------------------")
            
            go=False

initialize_crypto()
loop()
