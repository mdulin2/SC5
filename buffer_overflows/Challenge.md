
## Challenge 1
Firsty: Can you overflow my buffer? Overwrite the variable 'x' to get the flag. 

## Challenge 2
Dead: I don’t want to fix my buffer! Try to overwrite my buffer with the value 0xdeadbeef.
- Hint: Endianness is the tricky part here.
- Hint: GDB is amazing for debugging. Try to use it! :) 
- Hint: Use ``python3 -c "import sys; sys.stdout.buffer.write(b'A' * 0x1 + b'\x11\x22\x33\x44')" | ./dead``

## Challenge 3
killPtr: Can you overwrite the control flow? The goal is to corrupt the new ``functionPtr()`` in the structure to execute code at ``print_flag()``. 
- Hint: Use GDB to find the address of ``print_flag()``. 
- Hint: Use ``python3 -c "import sys; sys.stdout.buffer.write(b'A' * 0x1 + b'\x11\x22\x33\x44')" | ./killPtr``

## Challenge 4
corruptRet: Can you overwrite the control flow? The goal is to overwrite the previously stopped instruction pointer to jump to 'do_valid_stuff'. 
- Hint: How does the RET instruction pointer and stack work on x86?
- Hint: Use ``python3 -c "import sys; sys.stdout.buffer.write(b'A' * 0x1 + b'\x11\x22\x33\x44')" | ./corruptRet``
- Hint: The offset is 0x30 bytes


## Challenge 5
- There's no free ``win()`` function anymore. What will we do!? This time, you'll have to write a win function yourself with raw machine code! 
- Hint: The stack is executable. You can use your input to execute code. 
- Hint: Look up ``shellcode`` to pop a shell. You don't need to write this yourself. Later, when you have more time, you should though ;) 
- Hint: The address of the string is printed at the beginning of the program and is stack (ASLR is disabled). 
- Hint: Use ``(python3 -c "import sys; sys.stdout.buffer.write(b'A' * 1 + b'\x11\x22\x33\x44')"; cat -) | ./execStack``
