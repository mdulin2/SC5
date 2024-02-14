// https://stackoverflow.com/questions/55975895/stream-audio-over-websocket-with-low-latency-and-no-interruption


// Constants
var host = "localhost"
var http_port = "443"; 
var wss_port = "443"; 
var http_host = "https://" + host + ":" + http_port + "/api"; 
var wss_host = "wss://" + host + ":" + wss_port + "/websocket";


// Globals for the timed intervals. Required to cancel the operations
var higherLevelIntervalId = -1; 
var lowerLevelIntervalId = -1; 
var socketInitialized = false; 

// Websocket communication kept with the server for processing
var socket;  

// Call this function to setup the websockets
var oscillator1; 
var oscillator2; 
var audioPlayer = false; 

var number_tones = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
var entry_list = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]

other_dtmf = {
    "COIN" : [1700, 2200],
    "DIAL": [350, 440]
}

async function initializeCall(){
    const response = await fetch(http_host + "/startCall"); 

    var jsonData = await response.json();
    var call_id = jsonData['callId']; 

    // Create the websocket with a particular caller id
    socket = new WebSocket(wss_host + "/" + call_id);

    // Websocket is ready to go!
    socket.addEventListener("open",
        function(event){
            socketInitialized = true; 
        }
    ); 

    // Receive incoming messages
    socket.onmessage = function(e){
        receiveMessageWebSocket(e); 
    }

    document.getElementById("stateData").innerText = "State: DIALING";
    console.log(socket); 
}

// The bulky function that handles the websocket handling functionality
function receiveMessageWebSocket(event){
    var responseJson = JSON.parse(event.data);

    // TODO: Make more strict on location being sent to
    parent.postMessage(responseJson, "*");
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

            // Supported mimetypes: https://stackoverflow.com/questions/41739837/all-mime-types-supported-by-mediarecorder-in-firefox-and-chrome
            var mimeType="audio/webm";
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

                // Send webm data to the backend. Will convert into a 'wav' manually.
                socket.send(audioBlob);
            }

            recorder.start();

            // Every second, briefly stop the recorder in order to send the data within the 'onstop' handler.
            setTimeout(function() {
                recorder.stop();
            }, 420);
    }, 400);
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
    document.getElementById("numberData").innerText = "";
    document.getElementById("flagData").innerText = "";
    document.getElementById("stateData").innerText = "";
    document.getElementById("moneyData").innerText = "";

}

async function createPhoneBook(){
    var tableNode = document.getElementById("phoneTable");
    var response = await fetch(http_host + "/phoneBook"); 

    var responseJsonTmp = await response.json(); 
    var responseJson = responseJsonTmp['phoneBook'];

    // Iterate over each item in the phone book
    for (var rowIndex = 1; rowIndex < responseJson.length; rowIndex++){
        // https://www.w3schools.com/jsref/met_table_insertrow.asp
        var row = tableNode.insertRow(rowIndex);  // Add the row

        rowData = responseJson[rowIndex]; 

        // For each item that we want to add -- Name, phone and international or not
        for (var columnIndex = 0; columnIndex < rowData.length; columnIndex++){
            var cell = row.insertCell(columnIndex);
            if(columnIndex == 2){
                var cell = row.insertCell(columnIndex);
                cell.innerText = rowData[columnIndex] == "0" ? false : true;       
            }
            else{
                cell.innerText = rowData[columnIndex];
            }
        }
    }
}

function createDialNumbers(){

    var tableNode = document.getElementById("dialTable");

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
                generateButtonTone(number_tones[0][parseInt(rowIndex)], number_tones[1][parseInt(columnIndex)], 500)
            });

            cell.appendChild(btn);
        }
    }
}

/*
For a given button, generate a tone
https://marcgg.com/blog/2016/11/01/javascript-audio/
*/
function generateButtonTone(freq1, freq2, time){
    
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
    }, time); 
}

// Setup a postMessage listener for the 'dial' to 'index' communication
async function initializeIFrameListenerMainPage(){
    window.addEventListener('message', e => {

        // TODO: Wrong domain check
        console.log(e.origin, document.location.origin);
        if (e.origin !== document.location.origin) return;

        const key = e.message ? 'message' : 'data';
        const data = e[key];
        console.log("PostMessage Data:", data); 
        receiveMessage(data);  // Send to main page for update on the page
    },false);

    await createPhoneBook(); 
}

function receiveMessage(responseJsonAll){
    console.log("Post message received!")
    // link, flag, data, op

    // Iterate over all of the state changes in the list
    for(var i = 0; i < responseJsonAll.length; i++ ){

        var responseJson = responseJsonAll[i]; // Get a single entry

        // If a number or a data packet, then update the number on screen
        if(responseJson["type"] == "msg"){
            var numberP = document.getElementById("numberData"); 
            numberP.innerText = numberP.innerText + responseJson["data"]; 
        }
        else if(responseJson["type"] == "op"){
            var flagP = document.getElementById("stateData"); 
            if(responseJson["data"] == "EMERGENCY"){
                document.body.style.background = "red"; 
                flagP.innerText = "State:" + responseJson["data"]; 
            }
            // TODO: Add other coins here
            else if(responseJson["data"] == "QUARTER" || responseJson["data"] == "COIN" || responseJson["data"] == "NICKEL"){
                flagP.innerText = "State:" + responseJson["data"]; 
                var moneyP = document.getElementById("moneyData"); 
                moneyP.innerText = responseJson["state"]; 
                moneyP.style.visibility = "visible"; // Unhide the flag
            }
            else if(responseJson["data"] == "DIALING"){
                flagP.innerText = "State:" + "RINGING"
            }
            else if(responseJson["data"] == "CLEAR"){
                var numberP = document.getElementById("numberData"); 
                numberP.innerText = "Dialed Number: "; 
            }
            else{
                flagP.innerText = "State:" + responseJson["data"]; 
            }
        }
        else if(responseJson["type"] == "flag"){
            var flagP = document.getElementById("flagData"); 
            flagP.innerText = "Flag: " + responseJson["data"]; 
            flagP.style.visibility = "visible"; // Unhide the flag
        }
        else if(responseJson["type"] == "link"){
            var stateP = document.getElementById("stateData"); 
            if(responseJson["state"] != ""){
                stateP.innerText = "State: " + responseJson["state"];
            }
            else{
                stateP.innerText = "State: IN CALL"; 
            }

            var link = responseJson["data"]; 

            // Trigger to only allow a single call at a time
            if(audioPlayer == false){

                // Play the audio
                audioPlayer = new Audio(link);
                audioPlayer.play();          

                audioPlayer.addEventListener("ended", function(){
                    audioPlayer = false; // Allow the audio to be reused
                    stateP.innerText = "State: CALL ENDED"; 
                }); 
            }
        }
        else{
            console.log("Invalid change...", responseJson)
        }
    }
}


// https://stackoverflow.com/questions/58785295/use-javascript-to-record-audio-as-wav-in-chrome
// https://webaudiodemos.appspot.com/AudioRecorder/index.html
