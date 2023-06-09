## Decode Me 1
- The TPM command has three initial portions: 
	- Session tag - 2 bytes
	- Command Size - 4 bytes
	- Command Code - 4 bytes
- The information above is in Part 1 of the TPM 2.0 specification in the example payload within section 18.9
- Bytes 6-10 are 0x17b. This is the command code. 
- The command code name is within Part 2 of the TPM 2.0 specification. If you search '7b', you will find the Command Code table. 
- The command code table contains a single entry with 0x17b - TPM_CC_GetRandom. 
- 'TPM_CC_GetRandom' is the flag for this challenge.


## Decode Me 2
- We now how to decode the 'command' being used for the previous challenge. So, we should be able to decode the whole thing now. 
- This command code is 0x137, which corresponds to the nv_write command. 
- The next 8 bytes are handles, according to the documentation. 
- The next 4 bytes are the size of the 'auth' portion. This value is '0x9'.
- The next 9 bytes are the auth structure, as specified by the auth portion before this. 
- The next 2 bytes are the size of the following structure, the data being written as the flag! This is 0x1C in size. 
- The next 0x1C bytes are the string being written.
- If we hex to ascii decode this, we get ``SC5{Dec0de_the_hex_to_ascii}``.
- Alternatively, a simple hex to ascii would have shown the flag. 

## Decode Me 3
- We now how to decode the 'command' being used for the previous challenge. So, we should be able to decode the whole thing now. 
- This command code is 0x137, which corresponds to the nv_write command. 
- The next 8 bytes are handles, according to the documentation. 
- The next 4 bytes are the size of the 'auth' portion. This value is '0x24'. The flag is within the 'password' field, according to the prompt. 
- The first 4 bytes of the handle are the 'auth' field. These can be ignored. 
- After this, there is a size for the password (0x1a). 
- The password is hex encoded. If we use hex to ascii again, we'll get the flag. SC5{I_Am_A_Secret_Password}
- Flag: SC5{I_Am_A_Secret_Password}
