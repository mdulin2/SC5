
import asyncio
import websockets
import sys
import subprocess
import time
import os

from phone import handleDial, add_call


async def handlePhoneCall(websocket, path):
    async for message in websocket:

        print(path)
        # TODO Handle start call

        # TODO Receive the data and SAVE it as a wav to be parsed :) 
        # TODO Based upon the parsed data, now send it back - await websocket.send(message)
        
        filepath = "./live_recordings" + path + "-" + str(time.time())

        # Save the parsed message
        with open(filepath + ".webm", 'wb') as output_file:
            output_file.write(message)
        
        # Convert the file from 'webm' to 'wav' for processing
        subprocess.call(f'ffmpeg -i "{filepath}.webm" -vn "{filepath}.wav" -y -hide_banner -loglevel error', shell=True)

        call_id = path.replace("/", "")
        m = handleDial(filepath + ".wav", call_id)
        if(m != False and m != None):
            await websocket.send(m)
        
        # Remove the recordings
        os.remove(filepath + ".webm")
        os.remove(filepath + ".wav")
        #sys.exit(0) 

# Event loop for the websocket
asyncio.get_event_loop().run_until_complete(
    websockets.serve(handlePhoneCall, 'localhost', 8000))
asyncio.get_event_loop().run_forever()