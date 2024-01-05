## Challenge
- "Hey kids! Have you ever tried mining Bitcoin!? It's an easy way to make money! Do you know how it works?"
- You take some data and append data to the front until the 'hash' of the data has lots of zeros! 
- For this challenge, there is a server that you interact with via Python - you have a client program to use for this. All you need to worry about doing is sending the prepended data that created the hash with lots of zeros. 
- Write some code to prepend the starting 7 bytes with zeros. There is a (1/16)^5 probability this will work! You only have a minute to do so! :) Good luck!
- The only thing you need to modify is 'calc_hash()' within the template script. Everything else is there that you need and can be modified accordingly. The function should return the nonce needed for the hashing to succeed. If it's proper and is done under a minute, you will get the flag. 
- Hint: 
	- Just do it randomly. There's no better way.


