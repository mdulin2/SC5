## User Agent
- The 'user-agent' header is commonly used for an authorization restriction. 
- This is **bad** since the header can be spoofed. 
- This challenge is a web page with that restriction. Users need to set the 'user-agent' header properly to view the web page with the flag. 
- ``user-agent`` will be in the JavaScript code of the page. 
	- This forces kids to use the dev tools and learn how it works. 
- ``user-agent: CyberCupV`` seems reasonable to do.