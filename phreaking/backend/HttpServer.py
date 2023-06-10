
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

app.run(host='0.0.0.0', port=8001)