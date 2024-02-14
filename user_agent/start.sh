#!/bin/bash 

# Start all of the services
tmux new-session -d -s HTTPServer 'cd /webserver; python3 HttpServer.py'

# Sleep forever to continue this
sleep 100000000