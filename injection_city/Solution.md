# Solution 1 - Command Injection
- The command being executed is ``ping -c 1 <user_input>``. 
- This is being put directly into the ``subprocess`` command in Python and allows for bash metacharacters. 
- Once this is identified, it's as simple as running a bash command to print the flag. It should be noted that the command MUST be a valid command throughout the entire thing. 
- The input ``google.com; cat /flags/flag1.txt`` will end the original ping command (``;``) then use our own new command to print the flag. Put this into the ``domain`` field of the URL. This attack is known as ``command injection``, which is in the title of the challenge.
- Flag: SC5{pingpingpingping_wh0se_home!}

## Solution 2 - Argument Injection 
- In this challenge, we control the amount of bytes being read from the file. The command being executed is ``head -c <user_input> /tmp/test_file.txt``
-  In the previous challenge, shell metacharacters were allowed. In this challenge, that's not the case. So, we'll have to find an argument for the command ``head`` to print the flag. 
- The ``head`` command literally outputs the contents of a file. So, if we can inject an argument into the command, we can output the flag. 
- First, finish the ``-c`` flags value. This should be a number large enough to print the flag. 
- Next, put the path of the file you want to print; since we want to print the flag, we will put ``/flags/flag2.txt``. 
- The final input for the ``d`` parameter should be ``1000 /flags/flag2.txt``. 
- Flag: SC5{Michael_scarn_1n_tHe_injecti0n_c1ty!}


## Solution 3 - JavaScript Code Injection 
- Cross site scripting (XSS) is the act of injecting JavaScript into a web page that does not belong to you. By doing so, you can trick the browser to perform actions on behalf of the user, such as making a purchase or sending you their cookies. 
- The goal is to get the page to output an ``alert`` box by injecting your own JavaScript into the page. Just execute JavaScript with ``alert(1)`` to get the flag.
- There are several ways to do this: 
    - Use ``script`` tags. ``<script>alert(1)</script>``
    - Use ``onX`` event handlers within tags. ``<img onerror="alert(1)" src=x>``
    - If you see a payload that is popping an alert box but not giving a flag, feel free to give them the flag though. 
- Flag: SC5{JavaScript_in_the_page_is_Just_aS_bad!}

## Solution 4 - SQL Injection 
- SQL is a querying language for databases. SQL Injection is the act of changing the meaning of the query with user input. 
- The query is attempting to search for a particular value in the table. 
- This is done with the following query: 
```SELECT letter, info FROM search WHERE letter = '<user_input>'```
- If you give a single quote, an error is given. This is because the quote modifies the meaning of the query and messes up the syntax of it. 
- So, in order to modify the query, we need to get out of the string we are currently in. This is done using a single quote. 
- However, this does not quite work... we need to ensure that the rest of the query is valid. This can be done using a *comment* in SQL, ``-- ``. By adding a comment to the end, the query cancels out the rest of the data.
- The flag is within the tables ``flag``. So, we need to read from that table in order to get the flag.
- We cannot read data back from the original query since it won't have the proper table. So, we want to ADD content to the current query. 
    - A way to continue a query is with the *UNION* (https://www.w3schools.com/sql/sql_union.asp) clause. 
- Now, let's create a query that uses a UNION. 
    - The *id* of `'1 UNION select 1,1 -- `
    - This translates to the following query: 
        - SELECT letter, info FROM search WHERE letter '1 UNION select 1,1; -- ORDER BY id DESC;";`
    - This returns the data 1,1 (via the select clause ). Then, the `--` is a comment, cancelling the rest of the query. 
    - Why just 2 1's: 
        - The query returns FOUR fields. 
        - A UNION operator has to have the same number of fields to return in both the queries. 
- We know how to concatenate two queries now. 
- A NORMAL query to get the flag from the database would look like the following: 
    - ``select * FROM flag``.
- Now, we just need to do this in the UNION clause while making this a valid query. 
- ``1' UNION SELECT * from flag -- ``
    - The ``'`` is breaking out of the string. Then, we are selecting the flag from the table. Finally, we are using a comment to ensure that this is a valid call.
- Flag: SC5{InjectionCityIsForY0uA4D_M3!}


## Solution 5 - Template Injection 
- Template engines are used to present dynamic data into a web application. If a user can control the data being put into the templating engine, really bad things can happen, which is called template injection.
- In this challenge, the user can add their own code to the template engine language. This is shown via the ``render_template_string`` function. 
- A good test is using ``{{7*7}}``. This returns 49, which means that we have the ability to execute arbitrary code within the template language. 
- The variable ``flag`` is being added into the template. So, simply using ``{{flag}}`` will embed the flag variable as part of the outputted page. 
- Another solution is using something like https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection/jinja2-ssti. 
    - http://127.0.0.1:5000/name/?name=%7B%%20for%20x%20in%20().__class__.__base__.__subclasses__()%20%%7D%7B%%20if%20%22warning%22%20in%20x.__name__%20%%7D%7B%7Bx()._module.__builtins__[%27__import__%27](%27os%27).popen(%22cat%20/flags/*%22).read()%7D%7D%7B%endif%%7D%7B%%20endfor%20%%7D
- Flag: SC5{Don'tTrythisathomekdis}


## Solution 6 - Code Injection 
- Functions like ``eval`` and ``exec`` in Python allow dynamic generation and execution of Python code. If user input can be put into this, then arbitrary code execution can be performed on the server. This is called ``code injection``.
- The code being executed is ``"data['<user_imput1>'] = '<user_imput2>'" % (name, location)``
- The goal is to escape dictionary setting in order to change the meaning of the code being executed. In particular, we want to call ``print(flag)`` to get the flag.
- Putting a single quote causes a major error within any of the inputs. However, ``user_imput2`` is easier to work with so will we use that. After adding in a single quote, we can escape the context of the string. 
- Once there, we need to end the line. This can be done using a newline (%0A when URL encoded in the browser) or using a semicolon (;).
- Now that we have a new line, we can simply add in ``print(flag)``. 
- Finally, like the SQL injection challenge, we need to make the rest of the code valid. The easiest way to do this is to add a comment in Python ``#``. However, this needs to be URL encoded, which is %23. 
- Putting this altogether, we get ``'%0Aprint(flag)%23``. A semicolon can be used instead of the newline as well.
- Flag: SC5{AAAAAAAAAflag666666666666}