# Challenges for SC5 - Spokane Cyber Cup V

## Web 
- **Lottery**:
	- Redis duplicate key caching bug
- Korean food new auth issue(used first three years)
- **School Grade Book** (blackboard): 
	- Default creds leftover
	- Predictable credentials from pattern matching
	- Insecure Direct Object Reference (IDOR) on other students via IDs
- Regex Bypass Quiz 
- Host header injection for an email reset link 
	- Directory traversal to retrieve flag
- Client Side Trust of Bar Codes:
	- Bar codes hold data. But, this data is known and cannot be trusted by itself. 
- GraphQL (Kevin):
	- Bad authorization allows for the returning of too much data
- Known vulnerability exploit
- **amazon**(2): 
	- One time password fill up
	- Statistiics on this occuring
- **Racey**:
	- Race condition
- **Blackboard**:
	- Default creds
- SQL injection
- XSS
- CSRF
- IDOR
- Side channel
- Admin panel:
	- Insecure login (direct request or bad creds or SQLi maybe?) 
	- Command injection
- Insecure randomness
- Whatever else :) 


## Binary 
- **Binary Protections** (binary_protections):
	- DEP
	- Stack canaries
	- ASLR
- Basic memory corruption series: 
	- Corrupting a variable
	- Controlling the variable
	- Hijacking the control flow
	- Shellcode - your own code
	- ROP - pwnable.kr-like challenge
	- Use after free
	- https://github.com/mdulin2/SC3/tree/master/buf_series was used in years past. 
- Pickle Challenge: 
	- https://checkoway.net/musings/pickle/
- Integer overflow/underflow/truncation:
	- https://github.com/mdulin2/SMC2/tree/master/pokemon
	
## Linux 
- Linux usage basics
- **Error to Code** (error_to_code):
	- Turning an error message into perl code
- **Auth handler (auth_handler)**: 
	- Bypassing auth in a python script via unexpected input. In particular, negative indexingin Python.
- **No chars**
- Linux privilege escalation: 
	- 3 extras from last year here.
	- https://github.com/kratos1398/ctf_challenges
- **Odd**: 
	- Question mark wildcards

## Reverse Engineering 
- GameBoy:
	- Get the stuff working
	- Strings
	- Magic button combo
- Simple C binary reading

## Blue Team 
- Malware analysis or memory forensics (Gerard) 
- Wireshark packet analysis 
- Log Analysis 
- other blue team-y things?

## Cryptography
- Cesar Cipher
- **Digital Signature Algorithm (dsa)** (5): 
	- Explain DSA (manually verify) - will probably remove this one
	- Sign a message
	- What is the hard problem here? 
	- Recover private key from a known nonce. 
	- Recover private key from repeated nonces - Playstation 3 vulnerability 
- Signature bypass:
	- https://nft.mirror.xyz/VdF3BYwuzXgLrJglw5xF6CHcQfAVbqeJVtueCr4BUzs
- **Passphrase**
- Whatever Max Arnold wants to do? lol

## Other Challenges
- Hotel finding from only an image(Vanessa) 
- Blockchain challenges (Kevin)
- Location privacy issues via trianglation
- Morse Code
- Phreaking:
	- Unseen character
	- Long distance call
	- Things like this
	- https://www.instructables.com/ProjectMF-blue-box-phreaking-demo/
- Slide Rule:
	- https://www.sliderules.org/
- Soldering: Likely need funding and a custom PCB to do this one.
- I'm in video

