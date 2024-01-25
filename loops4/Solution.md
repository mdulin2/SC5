# Loops 4

This challenge asks the student to implement [elliptic curve point multiplication](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication). Two functions need to be used: point addition and point multiplication. The pseudocode for both algorithms is provided on Wikipedia

The most common bugs will likely be:

* Using standard division instead of modular inverse
* Forgetting to handle the point at infinity

The example in soln.py is a relatively clean implementation in Python that uses the special point (-1, -1) as infinity. This isn't great but should work. 

Alternatively, students can use a tool such as Sagemath to easily solve this problem.

```
E = EllipticCurve(GF(<modulus>), [<a>, <b>])
p = E(<pub_bx>, <pub_by>)
print(p * <priv_a>)
```
