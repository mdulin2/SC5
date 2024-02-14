
import asyncio
import sys
import subprocess
from flask import Flask, request
import flask
import js2py
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

flagfile = open("/flag.txt", 'r')
flag = flagfile.read()

js_code = open("/backend/code.js", 'r').read()
js2py.translate_file("code.js", "temp.py")

# Transformed code shown above...
from temp import * 

#curl http://localhost:8000/run_code -H "Content-Type: application/json" --data '{"data" : ["func1", "func2", "ROP", "func3", "func4", "0x8000000", "1337", "func5", "func6", "func7"]}'
@app.route('/run_code', methods=['POST'])
def run_code():

    # Assume this is JSON
    data = request.get_json()
    elements = data['data']

    # temp.executeCall(["func1", "func2", "ROP", "func3", "func4", "0x8000000", "1337", "func5", "func6", "func7"])
    result = temp.executeCall(elements)
    if(result == True):
        data = flag
    else: 
        data = "Nope :("

    response = flask.jsonify( {"status" : 200, "data" : data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response    

app.run(host='0.0.0.0', port=8000)