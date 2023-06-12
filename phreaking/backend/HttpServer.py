
import asyncio
import websockets
import sys
import subprocess
from flask import Flask
import flask

from phone import handleDial, add_call


app = Flask(__name__)
@app.route('/startCall')
def index():
    response = flask.jsonify( {"status" : 200, "callId": add_call()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

'''
TODO: Add 'coin' call here. 
Add money deposit to frontrun. 
Check to see if the 'coin' sound was made. If not, just ignore this. 
If it is, then add the coin like normal. 

If we see a coin add that WASN'T from this, then we can send over a flag. 
'''
## 

app.run(host='0.0.0.0', port=8001)