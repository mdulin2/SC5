// https://stackoverflow.com/questions/55975895/stream-audio-over-websocket-with-low-latency-and-no-interruption

// Constants
var host = "localhost"
var http_port = "8000"; 
var http_host = "http://" + host + ":" + http_port; 

async function authCall(){

    // Only checks the 'User-Agent' header. 
    // Expects the secret value of 'CyberCupV' as the user agent header
    const response = await fetch(http_host + "/auth"); 

    var jsonData = await response.json();
    var node = document.getElementById("access");

    if(jsonData['status'] === 200){
        node.innerText = 'flag: ' + jsonData['data']; 
    }
    else{ // 403 denied
        node.innerText = "Improper 'User-Agent' header. Good try!"; 
    }
}

authCall(); 
