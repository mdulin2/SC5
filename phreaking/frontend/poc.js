/*
Script for brute forcing phone calls
TODO: Fix the back end code to CONTINUE if the call ends AND it then hears this. 
WAR DIALING CHALLENGE. This may be too hard but is interesting for sure. 

TODO: Remove from the javascript that everyone can see from the challenge...
TOOD: Debug the function. Sometimes, it plays extra things and I'm unsure why...
*/

var easy_json = {
    "1" : [697, 1209],
    "2" : [697, 1336],
    "3" : [697, 1477],
    "4" : [770, 1209],
    "5" : [770, 1336],
    "6" : [770, 1477],
    "7" : [852, 1209],
    "8" : [852, 1336],
    "9" : [852, 1477],
    "0" : [941, 1336]
}

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

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function sendPhoneNumber(number){

    for(var i = 0; i < number.length; i++){
        digit = number[i]; 
        var frequencies = easy_json[digit]; 
    
        // Send for 500ms
        generateButtonTone(frequencies[0], frequencies[1], 500); 
        await new Promise(r => setTimeout(r, 1500));
    }

    generateButtonTone(350, 440, 1500); 
    await new Promise(r => setTimeout(r, 2500));
}

async function sendAllPhoneNumbers(){

    // Phone
    var beginning = "508"; 
    for(var i = 0; i < 5; i++){
        var number = beginning + i.toString().padStart(4,'0'); 
        console.log(number); 
        await sendPhoneNumber(number); 
        await new Promise(r => setTimeout(r, 10000));
    }
}
