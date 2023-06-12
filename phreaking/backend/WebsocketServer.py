
import asyncio
import websockets
import sys
import subprocess
import time
import os
import json

from phone import handleDial, add_call


async def handlePhoneCall(websocket, path):
    async for message in websocket:

        # Start call handled by HTTP        
        filepath = "./live_recordings" + path + "-" + str(time.time())

        # Save the parsed message
        with open(filepath + ".webm", 'wb') as output_file:
            output_file.write(message)
        
        # Convert the file from 'webm' to 'wav' for processing
        subprocess.call(f'ffmpeg -i "{filepath}.webm" -vn "{filepath}.wav" -y -hide_banner -loglevel error', shell=True)

        call_id = path.replace("/", "")
        m = handleDial(filepath + ".wav", call_id)

        # Only send back data if 'm' is useful.
        if(m != False and m != None):
            await websocket.send(json.dumps(m))
        
        # Remove the recordings
        os.remove(filepath + ".webm")
        os.remove(filepath + ".wav")

# Event loop for the websocket
asyncio.get_event_loop().run_until_complete(
    websockets.serve(handlePhoneCall, 'localhost', 8000))
asyncio.get_event_loop().run_forever()