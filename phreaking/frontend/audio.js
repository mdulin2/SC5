// https://stackoverflow.com/questions/55975895/stream-audio-over-websocket-with-low-latency-and-no-interruption


// Globals for the timed intervals. Required to cancel the operations
var higherLevelIntervalId = -1; 
var lowerLevelIntervalId = -1; 
var socketInitialized = false; 

// Websocket communication kept with the server for processing
var socket;  
var url = "localhost:8000"

// Call this function to setup the websockets
var oscillator1; 
var oscillator2; 

var number_tones = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
var entry_list = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]

// Initialize the numbers table
createDialNumbers(); 

async function initializeCall(){
    const response = await fetch("http://localhost:8001/startCall"); 

    var jsonData = await response.json();
    var call_id = jsonData['callId']; 

    // Create the websocket with a particular caller id
    socket = new WebSocket('ws://' + url + "/" + call_id);

    // Websocket is ready to go!
    socket.addEventListener("open",
        function(event){
            socketInitialized = true; 
        }
    ); 

    // Receive incoming messages
    socket.onmessage = function(e){
        receiveMessage(e); 
    }
    console.log(socket); 
}

// The bulky function that handles the websocket handling functionality
function receiveMessage(event){
    console.log("Received message!");
    console.log(event);
}

// Start or stop the audio processing
async function listenToAudio(){

    // Already listening
    if(higherLevelIntervalId != -1 || socketInitialized == true){
        return; 
    }

    await initializeCall();

    var media = await navigator.mediaDevices.getUserMedia({
        audio: true
    }); 
    
    higherLevelIntervalId = setInterval(startAudioParsing(media));
}

// The magic for the audio parsing
function startAudioParsing(stream) {

        // Start an interval counter which comes in and clears the other data and sends it off
        lowerLevelIntervalId = setInterval(function() {
            var chunks = [];
            var mimeType; 

            var supported = MediaRecorder.isTypeSupported("audio/webm;codecs=pcm");
            if(supported == true){
                mimeType = "audio/webm;codecs=pcm";
            }else{
                mimeType="audio/webm";
            }

            // Supported mimetypes: https://stackoverflow.com/questions/41739837/all-mime-types-supported-by-mediarecorder-in-firefox-and-chrome
            var recorder = new MediaRecorder(stream, {mimeType: mimeType});

            // Whenever there is data, push it to the 'chunks' queue
            recorder.ondataavailable = function(e) {
                chunks.push(e.data);
            };

            // When this stops, send the data over
            recorder.onstop = function(e) {

                // Convert 'blob' to wav mimetype before sending to server
                // https://stackoverflow.com/questions/52021331/convert-blob-to-wav-file-without-loosing-data-or-compressing
                var audioBlob = new Blob(chunks);
                console.log(audioBlob); 

                // Convert data to 'wav' (maybe) and send it off
                socket.send(audioBlob);
            }

            recorder.start();

            // Every second, briefly stop the recorder in order to send the data within the 'onstop' handler.
            setTimeout(function() {
                recorder.stop();
            }, 540);
    }, 500);
}


// Disable listening audio once a call has ended
async function cancelAudio(){

    // Are not listening at this point
    if(higherLevelIntervalId == -1){
        return; 
    }

    clearInterval(higherLevelIntervalId);
    clearInterval(lowerLevelIntervalId);
    socket.close(); 
    // TODO: Add 'endCall' function to stop the call on the backend

    higherLevelIntervalId = -1
    lowerLevelIntervalId = -1;
    socketInitialized = false; 
}

function createDialNumbers(){
    var tableNode = document.getElementById("dialTable")
    console.log(tableNode);

    for (var rowIndex = 0; rowIndex < 4; rowIndex++){
        // https://www.w3schools.com/jsref/met_table_insertrow.asp
        var row = tableNode.insertRow(rowIndex); 

        for (var columnIndex = 0; columnIndex < 3; columnIndex++){
            var number = entry_list[rowIndex * 4 + columnIndex]; 

            var cell = row.insertCell(columnIndex);
            cell.id = number; 
        
            // https://sebhastian.com/javascript-create-button/add
            let btn = document.createElement("button");
            btn.innerHTML = number;
            btn.id = number + "-" + rowIndex + "-" + columnIndex; 
            btn.addEventListener('click', function (e){
                var rowIndex = e.target.id.split("-")[1]; 
                var columnIndex = e.target.id.split("-")[2]; 
                
                // Call with the proper frequencies
                generateButtonTone(number_tones[0][parseInt(rowIndex)], number_tones[1][parseInt(columnIndex)])
            });

            cell.appendChild(btn);
        }
    }
}

/*
For a given button, generate a tone
https://marcgg.com/blog/2016/11/01/javascript-audio/
*/
function generateButtonTone(freq1, freq2){
    
    var context = new AudioContext()
    const oscillator1 = new OscillatorNode(context, { frequency: freq1 });
    const oscillator2 = new OscillatorNode(context, { frequency: freq2 });

    oscillator1.connect(context.destination);
    oscillator2.connect(context.destination);

    // Start the oscillators
    oscillator1.start(); 
    oscillator2.start(); 

    // Timer to stop the oscillators
    setTimeout(function(){
        // TODO: Make more gradual of a slow down to sound better
        oscillator1.stop(); 
        oscillator2.stop(); 
    }, 500); 

}