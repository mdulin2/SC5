//need to put the code into the box in the pamphlet

# Hints to give

* look at the code and find out how the object is signed

Sign the auth object for the user
def sign(username, random_nonce):
    '''
    Data to sign
Username | Session random data
    '''
    return sign_data(username + random_nonce)

# Solution

A digital signature is an electronic, encrypted, stamp of authentication on digital information such as email messages, macros, or electronic documents. A signature confirms that the information originated from the signer and has not been altered.

After looking at the source code, notice that the signature consists of a username and a random data merged together. That means, the signature for object  “A” and data “BC” is the same as for object “AB” and data “C”. 

1) create a user containing the word admin in it, for example: admin1
2) login as a user admin1 with random data 2
3) retrieve the session data and save a copy of it
4) load old session for "admin" with random data "12" and old signature saved 

![image](https://github.com/mdulin2/SC5/assets/48627556/98a22e25-b509-4f28-9d4c-d52398363623)
