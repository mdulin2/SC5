import re
from dataclasses import dataclass

@dataclass
class Curve:
    a: int
    b: int
    p: int

def add_point(ax, ay, bx, by, curve):
    # if a or b is infinity
    if ax == -1 and ay == -1:
        return bx, by
    elif bx == -1 and by == -1:
        return ax, ay

    if ax == bx and ay != by:
        # if a = -b
        return -1, -1
    elif ax == bx and ay == by:
        # point doubling
        lambd = (3*ax**2 + curve.a) * pow(2, -1, curve.p) * pow(ay, -1, curve.p)
    else:
        # point adding
        lambd = (by - ay) * pow(bx - ax, -1, curve.p)
    lambd = ((lambd % curve.p) + curve.p) % curve.p

    res_x = lambd ** 2 - ax - bx
    res_x = ((res_x % curve.p) + curve.p) % curve.p

    res_y = lambd * (ax - res_x) - ay
    res_y = ((res_y % curve.p) + curve.p) % curve.p

    return res_x, res_y

def mult_point(x, y, n, curve):
    # double and add method
    res_x = -1
    res_y = -1

    tmp_x = x
    tmp_y = y

    while n > 0:
        if n & 1 == 1:
            res_x, res_y = add_point(res_x, res_y, tmp_x, tmp_y, curve)
        tmp_x, tmp_y = add_point(tmp_x, tmp_y, tmp_x, tmp_y, curve)
        n >>= 1
    
    return res_x, res_y

def main():
    # This solution requires some copy-pasting.
    # I would have made it automatic, but it uses
    # an extremely nonstandard "ssh" interface
    # that cannot easily be scripted
    #
    # The multiplication and addition algorithms were
    # based on the pseudocode from wikipedia

    for i in range(5):
        l1 = input('paste 2 lines:')
        l3 = input()
        
        print('/')
        print(l1)
        print(l3)
        print('/')
        
        l1_matches = re.match(r'.* \+ (\d+)x \+ (\d+) \(mod (\d+)\)', l1)
        l3_matches = re.match(r'.* is (\d+) .*\((\d+), (\d+)\)', l3)

        a = int(l1_matches.group(1))
        b = int(l1_matches.group(2))
        mod = int(l1_matches.group(3))
        priv_a = int(l3_matches.group(1))
        pub_bx = int(l3_matches.group(2))
        pub_by = int(l3_matches.group(3))

        print(a, b, mod, priv_a, pub_bx, pub_by)
        curve = Curve(a, b, mod)
        res_x, res_y = mult_point(pub_bx, pub_by, priv_a, curve)
        print(f"{res_x},{res_y}")


if __name__ == '__main__':
    main()