Hints to give

* look at the code and find out how the object is signed

Sign the auth object for the user
def sign(username, random_nonce):
    '''
    Data to sign
Username | Session random data
    '''
    return sign_data(username + random_nonce)

Solution

When an object is signed, it uses a username and a user provided random value.

1) create a user containing the word admin in it, for example: admin1
2) login as a user admin1 with random data 2
3) retrieve the session data and save a copy of it
4) load old session for "admin" with random data "12" and old signature saved 
