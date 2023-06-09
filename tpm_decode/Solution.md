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
- Parse the password from the TPM command...
- Just build this myself in the tpm2 test tools and we should be good to go!

