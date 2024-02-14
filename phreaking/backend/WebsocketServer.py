import asyncio
import websockets
import sys
import subprocess
import time
import os
import json

from phone import handleDial
from dbHandler import initializeInformation
from random import randint

'''
Initialization process
'''
initializeInformation()

async def handlePhoneCall(websocket, path):
    async for message in websocket:

        path = path.replace("/websocket","")

        # Start call handled by HTTP        
        filepath = "./live_recordings" + path + "-" + str(time.time()) + "-" + str(randint(0,100000000000000000))

        # Save the parsed message
        with open(filepath + ".webm", 'wb') as output_file:
            output_file.write(message)
        
        
        # Convert the file from 'webm' to 'wav' for processing
        # Check return code
        subprocess.call(f'ffmpeg -i "{filepath}.webm" -vn "{filepath}.wav" -y -hide_banner -loglevel error', shell=True)

        call_id = path.replace("/", "")
        m = handleDial(filepath + ".wav", call_id)

        if(type(m) == dict):
            m = [m]

        # Only send back data if 'm' is useful.
        if(m != False and m != None):
            await websocket.send(json.dumps(m))
        
        # Remove the recordings
        os.remove(filepath + ".webm")
        os.remove(filepath + ".wav")

# Event loop for the websocket
asyncio.get_event_loop().run_until_complete(
    websockets.serve(handlePhoneCall, "0.0.0.0", 8000))
asyncio.get_event_loop().run_forever()
