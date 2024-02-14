from flask import Flask
from redis import Redis
#from numpy.random import randint
from flask_cors import CORS
from random import * 
import time

from apscheduler.schedulers.background import BackgroundScheduler 

app = Flask(__name__)
CORS(app)
sched = BackgroundScheduler(daemon=True) # Scheduler object 

# app.config['CORS_HEADERS'] = 'Content-Type'
redis = Redis(host='redis', port=6379, charset="utf-8", decode_responses=True)

def fetch_data_from_api(): 
    print("Generating new number...")

    # Set the history to have the old number
    old_num = redis.get("lottery")
    if(old_num != None):
        redis.lpush('history', old_num) 

    # Random number generation 
    number = randint(0, 100000000000) 
    redis.mset({"lottery": number})

# Cron job to generate a random number for the process
sched.add_job(fetch_data_from_api, 'cron', minute='*')
sched.start() 

@app.route('/')
def start():
    redis.incr('hits')
    return '{} times.'.format(redis.get('hits'))

@app.route('/register/<name>')
def register(name):
    redis.mset({name: 0})
    return 'User registered with name: {}'.format(name)

@app.route('/guess/<name>/<number>')
def guess(name, number):
    redis.mset({name: number})
    return 'User {} guessed: {}'.format(name, redis.get(name))

@app.route('/validate/<name>')
def validate(name):
    guessed = redis.get(name) # Get the user to validate
    if(guessed == None or redis.get("lottery") == None):
        return 'Wrong Person' 

    # If both keys exist, then check to see if they are the same
    if (int(redis.get("lottery")) == int(guessed)):
        
        contents = ""
        with open('flag.txt') as f:
            contents = f.read()
        return 'You guessed right! Your size is: {}'.format(contents)
    return 'Wrong guess'

@app.route('/history')
def history():
    return {'History': redis.lrange('history', 0, -1)}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
