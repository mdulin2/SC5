## Xorbitant

By XORing the first 4 characters of the ciphertext with the known start of the flag, the first few bytes of the key can be determined (`vZ8M`). Attempting to decrypt the whole message with keys of different sizes will give outputs that look very random and incorrect, except for length 6:

```
key: vZ8Ma      (len 5): b'SC5{<)^=\x1c_\x0c\x18+v5W\x06W]I/pt\x11rs\x0b\x137<isus!"Q'
key: vZ8Maa     (len 6): b'SC5{<>r_is\x1b#eall=\x0efrag-=e_if\x1b<isus!5}'
key: vZ8Maaa    (len 7): b'SC5{<>es\x0b\x067#rZ"{d"qI8\\\x16d^d0J\x0c\x07\'d,_!"Q'
key: vZ8Maaaa   (len 8): b"SC5{<>ed'dB\x0frZ5@*5(e8K-=e_if\x1b<~H;dx\x19j"
```

Notice that len 6 looks close to english. The next step is to figure out the key. This can be done by trying all combinations and looking for an output that looks correct, or by making guesses about other letters in the middle of the attempted decryption. For example, `frag-=e` could be `fragile`. Making the guess that the character at index 22 (`-`) should be an `i`, we can figure out that byte 4 (22 % 6) of the key is byte 22 of the ciphertext xor `i`. In this case, that gives a new guess of `vZ8M%a` giving the decryption

```
b'SC5{x>r_is_#eally\x0efragi=e_if_<isuse5}'
```

This looks closer. Guessing one more character gives the final key of `vZ8M%0`, and the flag of `SC5{xor_is_really_fragile_if_misused}`
