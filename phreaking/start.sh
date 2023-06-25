#!/bin/bash 

# Start all of the services
tmux new-session -d -s frontend 'cd /frontend; python3 frontendServer.py'
tmux new-session -d -s HTTPServer 'cd /backend; python3 HttpServer.py'
tmux new-session -d -s Websocket 'cd /backend; python3 WebsocketServer.py'

# Sleep forever to continue this
sleep 100000000