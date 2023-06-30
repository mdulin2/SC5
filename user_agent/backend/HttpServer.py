
import asyncio
import sys
import subprocess
from flask import Flask, request
import flask


app = Flask(__name__)

flagfile = open("/flag.txt", 'r')
flag = flagfile.read()

@app.route('/auth')
def auth():

    status = 403
    data = ""

    #if('User-Agent' in request.headers )
    print(request.headers) 
    for header in request.headers:
        key = header[0]
        value = header[1]

        print(key, value) 
        if('User-Agent' not in key): 
            continue 
        
        if("CyberCupV" in value ):
            data = flag
            status = 200

    response = flask.jsonify( {"status" : status, "data" : data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response    

app.run(host='0.0.0.0', port=8000)