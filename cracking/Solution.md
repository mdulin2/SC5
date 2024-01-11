## Hot and Heavy
The hash is an MD5 hash. This is given in the prompt but can be figured out from the size of the hash as well. Although it's impossible to go from the hash to the password directly, there are many lookup tables online with precomputed hashes for common values. 

So, if the hash is a common string, we can probably just look it up. Put the hash into 'https://crackstation.net/', which will output the password. 

flag: strongpassword

## A Pinch of Salt
The previous challenge allowed us to just lookup the hash directly. This is because it was a common string with nothing else inside of it. This time, the string we're hashing begin with the salt (extra prepended value) of "SC5:". So, the website crackstation and others will not work. 

This time, we're going to need a password brute forcing tool with a salt. JohnTheRipper is a good example for this. I found the example of 'https://github.com/aravindvaddi/password-cracking/blob/main/src/pwcrack-scripts/pwcrack.py' to work quite well with no modification besides the hash and salt to the script. If the rockyou.txt database is used, like referenced in the prompt, then the tool should find the password. 

flag: marthaluciadoctorcastro132006