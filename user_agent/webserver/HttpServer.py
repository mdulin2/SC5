
import asyncio
import sys
import subprocess
from flask import Flask, request
from flask import Flask, render_template
import flask


app = Flask(__name__)

flagfile = open("/flag.txt", 'r')
flag = flagfile.read()

@app.route('/')
def auth():

    status = 403
    data = ""

    #if('User-Agent' in request.headers )
    text = "Improper User-Agent header \"{}\". Good try!".format(request.headers["User-Agent"])
    print(request.headers) 
    image = "/static/knockingboy.jpg"
    for header in request.headers:
        key = header[0]
        value = header[1]

        print(key, value) 
        if('User-Agent' not in key): 
            continue 
        
        if("CyberCupV" in value ):
            text = flag
            status = 200
            image = "/static/kidInHouse.jpg"

    return render_template('index.html', text=text, image=image)

app.run(host='0.0.0.0', port=8000)