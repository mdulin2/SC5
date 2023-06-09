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
- Unpastable text box
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
- **Surrondings**: 
	- ulimit and error handling

## Reverse Engineering 
- GameBoy:
	- Get the stuff working
	- Strings
	- Magic button combo
- Simple C binary reading
- **tpm_decode** (3): 
	- Find the command
	- Find the secret being stored
	- Find the password in the command

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
- **Mean what you sign**: 
	- Misuse of signatures in cryptography

## Other Challenges
- Hotel finding from only an image(Vanessa) 
- Blockchain challenges (Kevin):
	- Attack tracing
	- NFT getting
- Location privacy issues via trianglation
- Morse Code
- Phreaking:
	- Unseen character
	- Long distance call
	- Things like this
	- https://www.instructables.com/ProjectMF-blue-box-phreaking-demo/
- Slide Rule:
	- Raven slide rule has a solver engine. Hosting ONLY this one and moving the verification to a backend would work pretty well.
	- https://www.sliderules.org/
- Soldering: Likely need funding and a custom PCB to do this one.
- I'm in video


## Contributing

- General notes: 
	- Be creative and have fun! Novel things are awesome :) 
	- You don't have to finish the challenge in one go. Feel free to put simple POCs or even ideas into its own folder.
	- There can only be so many difficult challenges. Generally, make things easier rather than harder. 
	- Try to limit the amount of external tools required. 
		- At SC4, the only required things were SSH, wireshark, a Unix terminal and a web browser. Lowest ever and worked really well.
		- If there's a specialized tool for something (like memory forensics), then we can do it. Just try to limit these as much as possible. Setting up new tools takes time to do and isn't always feasible for the high school teams. 
- Starting a challenge:
	- Each individual challenge or series of challenges should have its own folder. 
	- Mark the challenge on this README in the proper category.
	- For each sub-challenge, mark the vulnerability or overview of the challenge. 
	- Once it's finished, **bold** the challenge and update the total finished challenge amount.
- A prompt:
	- What are the students given? 
	- Hints should be put into here as well.
	- Usually put into the ``Challenge.md`` file. 
- A solution to the challenge. 
	- The overview of the solution is usually put into the ``Solution.md`` file. 
	- Anything else, such as a bash or Python script, can be put into the folder as well. 
- The setup for the challenge. 
	- If this is a hosted challenge, such as an SSH challenge or website, this should be in a docker container (if possible). If you're not comfortable with Docker, feel free to reach out to Maxwell Dulin. It is recommended that other Docker containers are reused for simplicity.  
	- If this is text, a file or anything else, the content should be uploaded and explained how it should be used. 


