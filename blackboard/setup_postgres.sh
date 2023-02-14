#!/bin/bash 

# Startup and initialize postgresql 
service postgresql start


# Queries to execute - create user and database
PGDATABASE="" PGPORT="" PGUSER="" PGHOST="" psql -c "CREATE USER rosario WITH PASSWORD 'rosariopwd';"

PGDATABASE="" PGUSER="" PGHOST="" psql -c "CREATE DATABASE rosariosisdb WITH ENCODING 'UTF8' OWNER rosario"

# Web request for database setup
curl http://localhost:80/InstallDatabase.php

exit 
