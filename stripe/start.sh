#!/bin/bash 

domain=$(jq '.domain' config.json -r)
sed -i "s/<PLACEHOLDER_HOST>/$domain/gi" frontend/code.js

# Start all of the services
tmux new-session -d -s frontend 'cd /frontend; python3 frontendServer.py'
tmux new-session -d -s HTTPServer 'cd /backend; npm install; node router.js'

# Sleep forever to continue this
sleep 100000000