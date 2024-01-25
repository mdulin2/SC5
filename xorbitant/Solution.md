## Xorbitant

By XORing the first 5 characters of the ciphertext with the known start of the flag, the first few bytes of the key can be determined (`v93"`). Attempting to decrypt the whole message with keys of different sizes will give outputs that look very random and incorrect, except for length 8:

```
key: v93"a      (len 5): b'SC5{ht\x02\x1ar!\x0b:;\n{#sN5~^(c}&X=\x1c\x0b5,h7<Md}'
key: v93"aa     (len 6): b'SC5{hcM\x10cb\x1cb~\x11)w+\x1ca&\x1b31>1\x177\rH5,h7<Ms2'
key: v93"aaa    (len 7): b'SC5{hcZ_is_biIlly_v~IgileOeN_mise\x7fMd}'
key: v93"aaaa   (len 8): b"SC5{hcZH&yN!iI{4<D$=Ip1>1\x177\rH5;0r'\x1f0%"
key: v93"aaaaa  (len 9): b'SC5{hcZH1!\x0b:;\n{4+\x1cv~^(c}&OeNH5,h7<Ms%'
```

Notice that len 7 looks close to english. The next step is to figure out the key. This can be done by trying all combinations and looking for an output that looks correct, or by making guesses about other letters in the middle of the attempted decryption. For example, `gile` could be `agile`, which would mean the last character of the key needs to be `a xor ciphertext[20] = I`. Then trying the key `v93"aaI` gives

```
b'SC5{hcr_is_bially_v~agileOef_mise\x7fed}'
```

which looks closer. Guessing a few more characters gets the final key of `v93"qmI`, and the flag of `SC5{xor_is_really_fragile_if_misused}`