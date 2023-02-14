//import data from "./data.json"; 

const data = {
	"url" : "http://localhost", 
	"port" : "8080", 
	"backend_url" : "http://localhost", 
	"backend_port" : "8081"
}

const backend_url = data['backend_url'] + ":" + data['backend_port']; 
console.log("Backend URL: ", backend_url); 

// if the buttons page, update the points every 5 seconds
// https://stackoverflow.com/questions/6944744/javascript-get-portion-of-url-path
if(window.location.pathname.indexOf("buttons.html")){
	var intervalId = window.setInterval(function(){
		print_points();
	}, 5000);
}

function create_button() {
	var oReq = new XMLHttpRequest();
	oReq.onreadystatechange = function() {
	
		if (oReq.readyState == XMLHttpRequest.DONE) {
			// Set the flag into the page 
			var button_res_json = JSON.parse(oReq.responseText); 
			var button_id = button_res_json['response']; 
			var success = button_res_json['success']; 

			if(success == 'true'){
				document.getElementById("button").innerHTML = "<p>Button ID:" + button_id + "</p>"; 
				
				// Sleep 3 seconds - then redirect
				sleep(3 * 1000).then(function(_){
					window.location.href = data['url'] + ":" + data['port'] + "/buttons.html?button_id=" + button_id; 
				}); 
			}else {
				document.getElementById("button").innerHTML = "<p>Error: " + button_res_json['error']['message'] + "</p>"; 
			}
		}
	}
	 
	// Setup the button creation request
	var req = backend_url + "/add_button"; 
	oReq.open("POST", req, true);
	oReq.send();
}

function press_button() {
	var oReq = new XMLHttpRequest();
	oReq.onreadystatechange = function() {

		// The request has succeeded
		if (oReq.readyState == XMLHttpRequest.DONE) {
			// Set the flag into the page 
			var button_res_json = JSON.parse(oReq.responseText); 
			var success = button_res_json['success']; 

			// Update the point amounts
			print_points();

			if(success == 'true'){
				var response_message = button_res_json['response']; 
				document.getElementById("message").innerHTML = "<p>Message:" + response_message + "</p>"; 
			}else{
				// Error...
				var error_message = button_res_json['error']['message']; 

				document.getElementById("message").innerHTML = "<p>Error Message:" + error_message + "</p>"; 

			}
		}
	}

	// Setup the button creation request
	var req = backend_url + "/submit";

	// Create the BODY of the request
	const urlParams = new URLSearchParams(window.location.search);
	var sub = {
		"press" : true, 
		"button" : urlParams.get("button_id")
	}; 

	oReq.open("POST", req, true);
	oReq.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
	oReq.send(JSON.stringify(sub));
}

function unpress_button() {
	var oReq = new XMLHttpRequest();

	// What to do upon finishing the call
	oReq.onreadystatechange = function() {

		// The request has succeeded
		if (oReq.readyState == XMLHttpRequest.DONE) {
			// Set the flag into the page 
			var button_res_json = JSON.parse(oReq.responseText); 
			var success = button_res_json['success']; 

			// Update the point amounts
			print_points();

			if(success == 'true'){
				var response_message = button_res_json['response']; 
				document.getElementById("message").innerHTML = "<p>Message:" + response_message + "</p>"; 
			}else{
				// Error...
				var error_message = button_res_json['error']['message']; 

				document.getElementById("message").innerHTML = "<p>Error Message:" + error_message + "</p>"; 
			}
		}
	}

	const urlParams = new URLSearchParams(window.location.search);

	// Get the button from the URL
	var button_id = urlParams.get("button_id");

	// Setup the button creation request
	var req = backend_url + "/" + button_id;
	oReq.open("DELETE", req, true);
	oReq.send();
}

// Display flag
function check_won() {
	var oReq = new XMLHttpRequest();
	
	oReq.onreadystatechange = function() {
		// The request has succeeded
		if (oReq.readyState == XMLHttpRequest.DONE) {
			// Set the flag into the page 
			var button_res_json = JSON.parse(oReq.responseText); 
			var success = button_res_json['success']; 

			if(success == 'true'){
				var response_message = button_res_json['response']; 

				document.getElementById("message").innerHTML = "<p>Message:" + response_message + "</p>"; 
			}else{
				// Error...
				var error_message = button_res_json['error']['message']; 
				document.getElementById("message").innerHTML = "<p>Error Message:" + error_message + "</p>"; 

			}
		}
	}

	// Setup the URL for the request
	var req = backend_url + "/winner/";
	const urlParams = new URLSearchParams(window.location.search);
	req = req + urlParams.get("button_id"); 

	// Setup the button creation request
	oReq.open("GET", req, true);
	oReq.send();
}

// Display the amount of points for the user
function print_points(){
	var oReq = new XMLHttpRequest();
	
	oReq.onreadystatechange = function() {
		// The request has succeeded
		if (oReq.readyState == XMLHttpRequest.DONE) {
			// Set the flag into the page 
			var button_res_json = JSON.parse(oReq.responseText); 
			var success = button_res_json['success']; 

			if(success == 'true'){

				var response_message = button_res_json['response'];

				// If more than 100 points, then get the flag!
				if(parseInt(response_message, 10) > 100){
					check_won();
				}
				 
				document.getElementById("points").innerHTML = "Points: <b>" + response_message + "</b>"; 
				
			}else{
				// Error...
				var error_message = button_res_json['error']['message']; 
				document.getElementById("message").innerHTML = "<p>Error Message:" + error_message + "</p>"; 
			}
		}
	}

	// Setup the URL for the request
	var req = backend_url + "/points/";
	const urlParams = new URLSearchParams(window.location.search);
	req = req + urlParams.get("button_id"); 

	// Setup the button creation request
	oReq.open("GET", req, true);
	oReq.send();
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}