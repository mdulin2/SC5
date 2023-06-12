## Recreate the phreaking process from the 70s. 

### Architecture
- Stream audio and process in small chunks: 
    - Doable! 
    - Would likely require a good amount of development work. 
    - Websockets to send audio every half second, process and figure out what to do? Like, what state does it change? 
- frontend: 
    - Press a button to change make tones
    - Listener that captures the audio data and sends it to the backend via a websocket in the webm format
    - In seperate iFrames because of same page audio weirdness
- backend: 
    - Audio processing using numpy number manipulation. Convert data from webm to wav
    - sqlite3 database to store the state of the caller
    - Websocket listener for audio data
    - HTTP server for everything else like starting the dialing process.


### Technology 
- Websocket frontend:
    - Native javascript. Doesn't support native 'wav' in the browser. 
    - Going to send data to the server and convert locally with ffmpeg
- Websocket backend: 
    - Python library like flask
- Audio processing: 
    - Raw data with numpy
    - Convert from webm from browser to wav with ffmpeg
- ffmpeg: 
    - Format converter


### PyAudio 
- Cross-platform audio processing: 
    - https://people.csail.mit.edu/hubert/pyaudio/
    - https://people.csail.mit.edu/hubert/pyaudio/docs/
- Bindings for *PortAudio*. So, need to install this on systems to use: 
    - MacOS M1: ``brew install portaudio``

### Tone Generator 
- Solo:
    - https://www.szynalski.com/tone-generator/
- DTMF: 
    - Numbers and everything are in it.
    - https://onlinetonegenerator.com/dtmf.html
- Multiple tone generator: 
    - https://onlinetonegenerator.com/multiple-tone-generator.html

### aubio
- Collection of tools for music and audio analysis
- Get pitch and amplitude: 
    - https://stackoverflow.com/questions/54612204/trying-to-get-the-frequencies-of-a-wav-file-in-python
- know your audio: 
    - https://towardsdatascience.com/get-to-know-audio-feature-extraction-in-python-a499fdaefe42

## Dependencies
- numpy
- ffmpeg
- flask 
- python3


## Phreaking
- Tones: 
    - 2600hz: 
        - Telephone operator connector tone - known as the blue box.
        - https://en.wikipedia.org/wiki/Blue_box
- Resources: 
    - Multi-frequency switching: 
        - https://en.wikipedia.org/wiki/Multi-frequency_signaling
    - History1: 
        - https://www.britannica.com/topic/phreaking
    - DTMF: 
        - https://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling
    - Tone information: 
        - https://www.tech-faq.com/frequencies-of-the-telephone-tones.html
    - Code info information about Bell Labs: 
        - https://telephoneworld.org/long-distance-companies/att-long-distance-network/old-att-operator-routing-codes/
    - Kinds of boxes: 
        - https://phreaking.fandom.com/wiki/List_of_boxes
    - Bell Labs Explanation on how this works: 
        - https://ia801606.us.archive.org/30/items/bstj39-6-1381/bstj39-6-1381_text.pdf


## Challenge Ideas
- Unseen character:
    - Type in a 'D' or something like that not on the screen 
    - Demonstrates the ability to create arbitrary tones
    - Currently, sending A, B, C or D will output a flag
- Long distance call: 
    - Type in a number like normal 
    - Use the 2600 frequency 
    - Pass in a long distance number
    - If right number, then send back the flag.
    - Blue box
- Coin tone: 
    - Pass in a quarter, dime or tone like that. 
    - Get a free call from using that. 
    - How to track REAL coin entry vs. fake one? Could store that as a field in the websocket? I don't people will know how to spoof this request anyway.
    - Red box
    - The different amount of tones reflected what type of coin to use. Unfortantly, my code can only pick out the frequencies and not clicks. Close enough though ;) 
    - Unsure HOW I'm going to implement this rn.
    - https://en.wikipedia.org/wiki/Red_box_(phreaking)
    - http://www.phonelosers.org/redbox/
- Computer discovery: 
    - Modem dials
    - Call forwarding
- Calling card fraud: 
    - Trying a bunch of calling cards... could be fun!


## Running
- frontend: 
    - ``cd frontend; ./start.sh``
- backend:
    - There are TWO things going on here. A websocket and HTTP flask server. They both need to be started.
    - websocket: ``python3 WebsocketServer.py``
    - HTTP: ``python3 HttpServer.py``


## TODO 
- Add phone book functionality
    - Have multiple callers that can be returned
    - Get funny audios to send over
- Long distance call validation:
- Integration coin into UI (or not):
    - Add request to VERIFY the process for coin being sent
    - If HTTP and websocket noise don't match, give them a flag.
- Update state change on UI
- Make UI look nice