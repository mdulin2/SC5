/*
Script that solves ALL of the challenges. 

It should be noted that there is no START CALL or END CALL noise at this moment. 
So, you must start and end the calls yourself.
*/

// All frequencies for 0-9
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

async function generateSingleTone(freq, time){
    var context = new AudioContext()
    const oscillator1 = new OscillatorNode(context, { frequency: freq });
    oscillator1.connect(context.destination);
    oscillator1.start(); 

    // Timer to stop the oscillators
    setTimeout(function(){
        oscillator1.stop(); 
    }, time); 
}

async function generateButtonTone(freq1, freq2, time){
    
    var context = new AudioContext()
    const oscillator1 = new OscillatorNode(context, { frequency: freq1 });
    const oscillator2 = new OscillatorNode(context, { frequency: freq2 });

    oscillator1.connect(context.destination);
    oscillator2.connect(context.destination);

    // Start the oscillators
    oscillator1.start(context.currentTime); 
    oscillator2.start(context.currentTime); 

    oscillator1.stop(context.currentTime + 0.5); 
    oscillator2.stop(context.currentTime + 0.5); 

    // Sleep for a brief moment
    await new Promise(r => setTimeout(r, time + 0.1)); // Sleep for this

}

async function sendPhoneNumber(number){

    for(var i = 0; i < number.length; i++){
        digit = number[i]; 
        var frequencies = easy_json[digit]; 
    
        // Send for 500ms
        await generateButtonTone(frequencies[0], frequencies[1], 500); 

        // Why does this timeout need to be sooo long? I don't understand this?
        await new Promise(r => setTimeout(r, 1500));
    }

    generateButtonTone(350, 440, 1500); 
    await new Promise(r => setTimeout(r, 2500));
}

async function sendPhoneCallingCard(number){

    // Dial '7' to call the card number line
    for(var i = 0; i < 1; i++){
        var frequencies = easy_json["7"]; 

        // Send for 500ms
        await generateButtonTone(frequencies[0], frequencies[1], 500); 
    }

    await new Promise(r => setTimeout(r, 1000)); // Sleep for this

    // Send the 'dial' tone
    generateButtonTone(350, 440, 500); 
    await new Promise(r => setTimeout(r, 2500));

    for(var i = 0; i < number.length; i++){
        digit = number[i]; 
        var frequencies = easy_json[digit]; 
    
        // Send for 500ms
        await generateButtonTone(frequencies[0], frequencies[1], 500); 

        // Why does this timeout need to be sooo long? I don't understand this?
        await new Promise(r => setTimeout(r, 1500));
    }

    generateButtonTone(350, 440, 1500); 
    await new Promise(r => setTimeout(r, 2500));
}

/*
Challenge 4 POC 
Need to manually 'startCall' though. Could fix this.
*/
async function sendAllPhoneNumbers(){

    var beginning = "789"; 
    for(var i = 0; i < 50; i++){ // Perform this call over and over again
        var number = beginning + i.toString().padStart(4,'0'); 
        console.log(number); 
        await sendPhoneCallingCard(number); 
        await new Promise(r => setTimeout(r, 10000));
    }
}

// Challenge 3
async function bluebox(){

    // Send a valid number
    await sendPhoneNumber("2051234"); 

    // 2600 tone - sets up a DISCONNECT
    generateSingleTone(2600, 1000); 
    await new Promise(r => setTimeout(r, 2000)); // Sleep 

    // Valid call to an international number
    await sendPhoneNumber("648379998756"); 
    await new Promise(r => setTimeout(r, 2000)); // Sleep 

    // Flag should appear
    console.log("Flag should be here... unless something went wrong"); 
}

// Challenge 2 - There are a few tones that can do this
async function redbox(){
    var buttonExec; 

    for(var i = 0; i < (5 / .25 * 2); i++ ){
        buttonExec = () => {generateSingleTone(800, 500)}; // Quarter
        //buttonExec = () => {generateButtonTone(1700, 2200, 500)}; // COIN
        //buttonExec = () => {generateButtonTone(1050, 1100, 500)}; // Nickel
        buttonExec(); 
        await new Promise(r => setTimeout(r, 1500)); // Sleep 
    }
}

// Challenge 1 - playing the unscene tones
async function ABCD(){
    // A few different tones will work. Putting all of them here for good measure
    // "A: 697,1633", "B: 770, 1633", "C: 852, 1633", "D: 941, 1633". 
    await generateButtonTone(697, 1633, 500); // A
    await generateButtonTone(770, 1633, 500); // B
    await generateButtonTone(852, 1633, 500); // C 
    await generateButtonTone(941, 1633, 500); // D
}


/*
TODO: Add programatic solution to ALL of the challenges
*/
