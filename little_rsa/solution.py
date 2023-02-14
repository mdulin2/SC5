

import sympy.ntheory
import random


#setup
bits = 96
e = 37
msg = int.from_bytes(b'SC4{euler!}', 'big')

p = random.randint(1, 2**(bits//2)) | 1
while not sympy.ntheory.isprime(p) or (p-1) % e == 0:
    p = random.randint(1, 2**(bits//2)) | 1

q = random.randint(1, 2**(bits//2)) | 1
while not sympy.ntheory.isprime(q) or (q-1) % e == 0:
    q = random.randint(1, 2**(bits//2)) | 1

c = pow(msg, e, p*q)

#prompt
print(f"p: {p}")
print(f"q: {q}")
print(f"N: {p*q}")
print(f"e: {e}")

print(f"secret message: {c}")
print(f"Can you find the original message?")

p = 157313963367733
q = 205183854424553
N = 32278285358594391272643148349
e = 37 
c = 30062997357812254050845754858

#solution
d = pow(e, -1, (p-1) * (q-1))
print(f"d: {d}")
recovered = pow(c, d, p*q)
print(recovered)
print(f"recovered message: {recovered.to_bytes(bits//8, 'big')}")

