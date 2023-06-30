# General 
- Learn about the technology and look at issues with dynamic strings being used. 
- The easiest way to modify the data is to take the string and modify it inline with your input. 
- Besides modifying the data, the rest of the data has to be valid after the modification. 

## Command Injection - Challenge 1
- The program is running a bash command. Can you hijack the command? 
- The command is ``ping -c 1 <Your input>``
- The flag is at ``/flags/flag1.txt``

## Argument Injection 
- The program is running a command via ``execve`` and NOT using bash commands. This means that bash characters, such as ``*`` and others no longer work. Can you cause the program to return the flag without bash meta characters? The command being executed is ``head -c <<User Input>>``
- The flag is at ``/flags/flag3.txt``
- Hint: What options does the. 

## Template Injection 
- The website is using a templating engine for adding data to the HTML. What if you could modify the templating language itself? This is using the Jinja2 templating language.
- The flag is at ``/flags/flag2.txt``
- Hint: The template has injected the variable ``flag`` into the environment. 

## Code Injection 
- The website is using ``exec()`` in Python in order to take user input for the key and value of a dictionary. The code being added into ``exec()`` is ``data['<<INPUT1>>'] = '<<INPUT2>>'``. 
- The flag is at ``/flags/flag4.txt``


## JavaScript Code Injection 
- The input being reflected into the page is not being sanitized. What if we could add javascript into the page to execute code? This is known as <i>cross-site scripting</i>. 
- The flag will return if the XSS was completed successfully. 

## SQL Injection 
- There is search functionality for looking at the alphabet. There is a SQL injection within the search functionality. The query is ``SELECT letter, info FROM search WHERE letter = '<<Your Input>>'``. 
- The flag is in the SQL table ``flag``. Take the flag from the table. 

