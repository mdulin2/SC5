
import asyncio
import sys
import subprocess
from flask import Flask, request
import flask
import js2py


app = Flask(__name__)

flagfile = open("/flag.txt", 'r')
flag = flagfile.read()

js_code = open("/backend/code.js", 'r').read()
execute = js2py.eval_js(js_code)

@app.route('/run_code')
def run_code():


    execute()
    #print(res_2(5))

    data = []
    response = flask.jsonify( {"status" : 200, "data" : data})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response    

app.run(host='0.0.0.0', port=8000)