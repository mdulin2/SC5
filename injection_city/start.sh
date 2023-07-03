#!/bin/bash 

# Start all of the services
tmux new-session -d -s frontend 'cd /app; python3 /app/app.py'

# Sleep forever to continue this
sleep 100000000
