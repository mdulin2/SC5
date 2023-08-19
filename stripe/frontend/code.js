// https://stackoverflow.com/questions/55975895/stream-audio-over-websocket-with-low-latency-and-no-interruption

// Constants
//var host = "<PLACEHOLDER_HOST>"
var host = "localhost"
var http_port = "5000"; 
var http_host = "http://" + host + ":" + http_port; 

async function loginUser(){
    var username = document.getElementById('username').value;
    console.log(username); 
    
    const rawResponse = await fetch(http_host + "/login", {

        method: 'POST',
        headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
        },
        body: JSON.stringify({"user" : username})
    });

    var jsonData = await rawResponse.json();
    if('ID' in jsonData){
        window.location.href = `/store.html?user=${jsonData['ID']}`
    }    
    else{
        document.getElementById('error').innerText = `${jsonData['ID']} is an invalid user.`
    }
}

async function buy(){
    const queryString = window.location.search;
    const urlParams = await new URLSearchParams(queryString);
    console.log(urlParams); 
    var username = urlParams.get('user');
    console.log(username);
    if(username === undefined){
        // TODO - handle error
        console.log("User dne");
        return;
    }
    
    const rawResponse = await fetch(`${http_host}/stripe/${username}`, {
        method: 'POST'
    });
    
    var jsonData = await rawResponse.json();
    console.log(jsonData); 

    // TODO - handle too many and bad username case here
    if(jsonData['id'] === undefined){
        document.getElementById('error').innerText = `${jsonData['ID']} is an invalid request`;
        return; 
    }

    document.getElementById('error').innerText = `Sending user to Stripe`;

    var stripe_direct = jsonData['redirect_url']; 
    // Your application has indicated there's an error
    window.setTimeout(function(){

        // Move to Stripe.
        window.location.href = stripe_direct;

    }, 5000);
}

async function autoRedirect(){
    const queryString = window.location.search;
    const urlParams = await new URLSearchParams(queryString);
    var username = urlParams.get('user');

    document.getElementById('error').innerText = `Sending user back to store`;

    // Your application has indicated there's an error
    window.setTimeout(function(){

        // Move to Stripe.
        window.location.href = `/store?user=${username}`;

    }, 5000);  
}

// Get the existing orders of a user
async function getOrderData(){
    await getAllOrders(); 
    await getCompletedOrders();
}

async function getCompletedOrders(){
    const queryString = window.location.search;
    const urlParams = await new URLSearchParams(queryString);
    console.log(urlParams); 
    var username = urlParams.get('user');
    console.log(username);
    if(username === undefined){
        // TODO - handle error
        console.log("User dne");
        return;
    }
    const rawResponse = await fetch(`${http_host}/user/${username}`, {
        method: 'GET',
    });

    var jsonData = await rawResponse.json();
    console.log(jsonData);
    document.getElementById('storeTitle').innerText = `Buy 'Gerald Hitman' Services (${jsonData['Amount']}/2)`;
}
async function getAllOrders(){
    const queryString = window.location.search;
    const urlParams = await new URLSearchParams(queryString);
    var username = urlParams.get('user');
    if(username === undefined){
        // TODO - handle error
        console.log("User dne");
        return;
    }
    const rawResponse = await fetch(`${http_host}/orders/${username}`, {
        method: 'GET',
    });

    var responseJson = await rawResponse.json();
    console.log("Table json:", responseJson); 

    var tableNode = document.getElementById("orderTable");

    // Iterate over each item in the order table
    for (var rowIndex = 1; rowIndex < responseJson.length + 1; rowIndex++){
        // https://www.w3schools.com/jsref/met_table_insertrow.asp
        var row = tableNode.insertRow(rowIndex);  // Add the row
        console.log("In loop upper loop...")
        rowData = responseJson[rowIndex]; 
        var cell1 = row.insertCell(0); 
        var cell2 = row.insertCell(1);
        cell1.innerText = rowData['ID'];
        console.log(rowData["Session"]); 
        cell2.innerHTML = `<a href="${rowData["Session"]}">Stripe</a>`
    }
}