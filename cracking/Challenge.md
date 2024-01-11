## Hot and Heavy
- A <i>hash</i> is a one way function. This means that once the hash has been generated, it's impossible to get back the original input. For passwords, it's more secure to store them as a hash in the case of a data breach. Imagine, you've hacked into NASA and stolen some hashes. Can you get back the original password? The flag is the original text for the h as below: 

MD5: f93fc10472a31bb3061aa0b45e228c5a

## A Pinch of Salt
- This time, you can't just <i>look up</i> the hash. The hash is a little bit harder. Can you find the hashed value with a prefixed salt of "SC5:"?
- A <i>salt</i> is a value used before the data being hashed. For instance, if "SC5:" is the salt, then the return of the data would come after it. This could be "SC5:Monkey123".
- Hash: e2cfa55773e02dc582ef1c57cce1575d7c70cd5026efdaefc7de27d9d455064d
marthaluciadoctorcastro132006
- Hint: You may need to write a script or use a tool to do this. Feel free to find a script/tool online or make one yourself in Python.
- Hint: Use the [https://github.com/zacheller/rockyou/blob/master/rockyou.txt.tar.gz](rockyou.txt)' wordlist for this.