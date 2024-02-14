#!/bin/bash 

# Disable ASLR
echo 0 | tee /proc/sys/kernel/randomize_va_space

service ssh restart && sleep 5d