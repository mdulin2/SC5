## Challenge 0 - RSA math 
- Given all of the components of RSA, encrypt a small message :) 
- Hint: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- Hint: 
```
p: 23
q: 29
N: 667
e: 3
d: 411
Message: 101
```

## Challenge 0.5 - RSA Math reverse
- Given all of the components of RSA, **decrypt** a small message :) 
```
p: 23
q: 29
N: 667
e: 3
d: 411
Encrypted message: 289
```

## Challenge 1 - Recover d
- RSA made the modern online store what it is today. Without RSA, the transmission of keys and encryption would be impossible. 
- In this case, we KNOW all the values besides 'd'. Can you recover 'd' to decrypt the message?
```
p: 157313963367733
q: 205183854424553
N: 32278285358594391272643148349
e: 37
secret message: 30062997357812254050845754858
```

## Challenge 2 - Recover the message
- RSA made the modern estore what it is today. Without RSA, the transmission of keys would be impossible. 
- Using 'd' from the previous challenge, recover the original message.
- Hint: ``plaintext_message = (ciphertext ^ d) mod N`` 

## Challenge 3 - Recover the text
- With the right message, you can now go from the message back to the ASCII text
- Hint: The Python code to go from the bytes to the message was ``msg = int.from_bytes(b'SC4{FLAG}', 'big')``. Now, do the reverse.



