from flask import Flask, render_template, request, render_template_string, request
from markupsafe import Markup
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
from SimpleSql import * 

'''
Add REAL spaces
Make the container 'readonly' except for a tmp directory with the databases

Challenges to add: 
- NoSQLi
'''

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html') 

# Command injection challenge code
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

   return render_template('ping.html',contents=output, command=command, error=error, domain=domain) 


# Argument injection challenge code
@app.route('/head/')
def head():
   d = request.args.get('d')
   if(d == None):
      return "Please add commands to the 'd' parameter"

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag2 user
   os.setuid(1001)

   command = "head -c %s /tmp/test_file.txt" % d
   command_split = command.split(" ")
   print(command) 

   p = subprocess.Popen(command_split, stdin=PIPE, stdout=PIPE, stderr=PIPE, encoding="utf-8") 
   output, error = p.communicate()
   return render_template('head.html', contents=output, error=error, command=command)



# JavaScript Code injection challenge code
@app.route('/xss', methods=["GET", "POST"])
def xss():
   data = ""
   if 'input' in request.form:
      data = request.form['input']

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)
 
   # flag3 user
   os.setuid(1002) 

   html = render_template('xss.html', userInput=Markup(data), flag=None)
   if(parse_xss(html) == True):
      # Read the flag in - can reference the flag as an object now.
      flagfile = open("/flags/flag3.txt", 'r')
      flag = flagfile.read()
      return render_template('xss.html', userInput=Markup(data), flag=flag)
   else: 
      return html
   
## SQL injection challenge code
## Solution: "' UNION select * from flag; -- "
@app.route('/search', methods=["GET", "POST"])
def search():

   search = ""
   if 'search' in request.form:
      search = request.form['search']

   ## Username and password field ## 
   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)
 
   # flag4 user
   os.setuid(1003) 

   query = ""
   if(search != ""):
      # Add search information into query from user here
      query = "SELECT letter, info FROM search WHERE letter = '" + search + "'"

   sql_response = ""
   if(search != ""):
      rows = searchDb(query) 
      sql_response = rows

   return render_template('search.html', userInput=query, flag=None, response=sql_response)

# Template injection
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
   <h1>What's your name? - Template Injection</title>
    <pre>Input for jinja2 flask templating: %s</pre>
  </body>
</html>
""" % (name) 

   if(os.fork() != 0):
       time.sleep(5)
       sys.exit(1)

   # flag5 user
   os.setuid(1004) 

   # Read the flag in - can reference the flag as an object now.
   flagfile = open("/flags/flag5.txt", 'r')
   flag = flagfile.read()

   return render_template_string(t, flags=flag, flag=flag)


# Code injection - exec
# http://127.0.0.1:5000/building_data?name=a&address=%27%0Aprint(open(%27/flags/flag4.txt%27).read())%0A%27
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
 
   # flag6 user
   os.setuid(1005) 

   # Read the flag in - can reference the flag as an object now.
   flagfile = open("/flags/flag6.txt", 'r')
   flag = flagfile.read()

   # Set the group in order to restrict the permissions
   command = "data['%s'] = '%s'" % (name, location)
   f = StringIO()

   result = ""
   error = ""
   try:
      with redirect_stdout(f):
         exec(command) # Dynamically execute our code
      result = f.getvalue()
   except Exception as e:
      print(e)
      error = "Error: " + str(e)

   return render_template('code.html', contents=result, error = error, command=command)

'''
XSS Challenge helper functions. 
Determines whether XSS has occurred or not.
'''
def filter_on_event(tag):
   if(tag.name != "span"):
      return False

   childTags = tag.findChildren()

   for tag in childTags:
      keys = list(tag.attrs.keys())
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
              parser = Parser()
              tree = parser.parse(data)
              for node in nodevisitor.visit(tree):
                    if 'alert(' in node.to_ecma():
                       return True

   return False

if __name__ == "__main__":
   create_table()
   addData()

   app.run(host='0.0.0.0', port=5001)
