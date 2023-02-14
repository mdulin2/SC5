## Info.md 

This folder is a buffer overflow series that is meant to walk through the students in a more simple manner. In previous years, the redirect of the execution was too much to understand right off the bat (endian, stack, eip, ASLR, etc.). So, this year, we are doing a series to make this problem more approachable.   
  
- Challenge 1: firsty.c
	- Simply just overwrite ANY in the integer variable to get the flag 
- Chalelnge 2: dead.c 
	- This time, the overwritten integer must be a very specific value: 0xdeadbeef. 
	- This is in order to teach the student about stack alignment and endianness. 
- Challenge 3: redirect.c 
	- Redirect the execution of the program to an easy 'win' function.
	- This is the first REAL buffer overflow that does anything that legit. 
	- The EIP (x86) must overwritten to the value of the 'win' function with the proper endianness and location. 
- Challenge 4: big_time.c (stretch?) 
	- Redirect execution of the program to shellcode (on the stack). 
	- This forces the student to understand how the stack works, assembly writing, how to write 'actual bytes' and the beginning basics of pwn :)
