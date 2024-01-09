from time import sleep
from sage.all import *
import random


def print_header():
    prompt = '''Remember me? I *still* like loops!
Mathematicians have come up with lots of clever ways of making loops.
Instead of just multiplying numbers, they made a new operation that
lets you "add" points on a weird squiggle called an Elliptic Curve.

You can "add" two points by drawing a line through them, finding the
only other point where the line intersects the curve, and then flipping
the Y coordinate to be negative. Or you can just look up the formula
online.

You can do "multiplication" of points just like with normal numbers by
"adding" a point to itself over and over. Just like with multiplying for
RSA, this makes a loop, which we can use for cryptography.

To start off, we'll agree on a point called G on the elliptic curve.
Pick a secret number, call it a. I'll pick a different secret, called
b. You can send me a * G, and I'll send you b * G. Then you can
"multiply" my message (b * G) by a, and I can "multiply" yours by b.
You'll get (b * G) * a and I'll get (a * G) * b. Both of those are equal
to a * b * G, so we now have a shared secret value.

'''
    for line in prompt.splitlines():
        print(line)
        sleep(0.1)

def print_flag():
    print('SC5{is_this_a_mathematical_group?}')

def gen_prompt(bitlen: int):
    # make a prime
    modulus = random.randint(2**(bitlen - 1), 2**bitlen - 1)
    while not is_prime(modulus):
        modulus = random.randint(2**(bitlen - 1), 2**bitlen - 1)
    
    a = random.randint(1, min(modulus - 1, 300))
    b = random.randint(1, min(modulus - 1, 5000))

    E = EllipticCurve(GF(modulus), [a, b])
    g = E.gens()[0]

    priv_a = random.randint(1, g.order() - 1)
    priv_b = random.randint(1, g.order() - 1)

    pub_b = priv_b * g
    solution = priv_a * pub_b
    while solution.is_zero():
        priv_b = random.randint(1, g.order() - 1)
        pub_b = priv_b * g
        solution = priv_a * pub_b

    print(f"On the elliptic curve y^2 = x^3 + {a}x + {b} (mod {modulus})")
    print(f"where the point G = ({g[0]}, {g[1]})")
    print(f"if your secret (a) is {priv_a} and I give you the point ({pub_b[0]}, {pub_b[1]})")
    print(f"what is the shared secret? (Give the coordinates as \"x,y\")")

    guess = input()
    parts = guess.split(',')
    guess_x = int(parts[0].strip())
    guess_y = int(parts[1].strip())

    return solution[0] == guess_x and solution[1] == guess_y
    
def fail():
    print('nope')
    exit()

def main():
    try:
        print_header()

        print('1/6')
        if gen_prompt(6):
            print('correct\n')
        else:
            fail()

        for i in range(2, 5):
            print(f"{i}/6")
            # guarantee the generator a few times to make the pattern easier to spot

            if gen_prompt(7 + i):
                print('correct\n')
            else:
                fail()

        print('6/6')
        print('Final challenge:\n')

        if gen_prompt(48):
            print_flag()
        else:
            fail()

    except ValueError:
        print('invalid')


if __name__ == '__main__':
    main()
