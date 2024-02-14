
import asyncio
import websockets
import sys
import subprocess
from flask import Flask
import flask
from dbHandler import get_phone_book_info

from phone import handleDial, add_call


app = Flask(__name__)
@app.route('/api/startCall')
def startCall():
    response = flask.jsonify( {"status" : 200, "callId": add_call()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/stopCall')
def stopCall():
    response = flask.jsonify( {"status" : 200, "callId": add_call()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/phoneBook')
def getPhonebook():
    response = flask.jsonify( {"status" : 200, "phoneBook" : get_phone_book_info()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response    


app.run(host='0.0.0.0', port=8001)