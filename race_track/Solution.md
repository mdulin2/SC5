## Solution 
- There is a basic explanation below. A more technical one will follow: 
	- NOTE: This is an unbelievably complex problem. Unless you want to learn about GLibC malloc internals, I would move on. 
- But, the payload.py has a solution for this challenge that works, if the default setup for GLibC is 2.23 (ubuntu 16.04)
- Concepts to this attack: 
	- Unsorted bin attack 
	- Use after free (read and write) 
	- Defeating stack canaries 
	- One Gadget (easy pop shell) 
	- Basic assembly understand (stack, ESP, etc.) 

## Basic Explanation 
Strategy: 

- UAF on sponsor update
	- Create two sponsors (one to UAF and the other to keep from consolidating with the top) 
	- Free the first one 
	- We have control over of bytes 8-16 on this struct. 
- Update the bk pointer of the `sponsor_counter` via the UAF in the previous step that we discussed.
	- This is the `rank` of a racer 
- Unsorted bin attack on the global counter of the sponsors array (non-pie) 
	- Do this by allocating another racer. This triggers the unsorted bin attack
- View the sponsor count: 
	- Because we overwrote the sponsor count before, this will have an address to GLibC! 
	- Use this as the GLibC leak for later on for the one_gadget
- View 12th sponsor to leak stack cookie 
- Update the 12th sponsor: 
	- Edit the ret pointer. The last 8 bytes of the string are the pointer. 
	- However, this changes the rest of the sponsors values...
- Select the race option!: 
	- This allows us to set the value of the 12th sponsors stack cookie.
	- Do this to ensure that the buffer overflow check passes
	- The `grade` of the sponsor should be set to the stack cookie. 
- Quit: 
	- The quit will take us to the pointer that we originally set a while ago. 
	- Code exec! Use the libc leak to one gadget to a shell :) 
	- The first one_gadget from the current version of libc (that we use) works with this! 
