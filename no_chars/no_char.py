#!/usr/bin/python

import os
import pwd

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def is_valid(user_input):
	if(len(user_input) != 0):
		return False

	return True


def run():
	print(get_username())

	print('uid,euid =',os.getuid(),os.geteuid())
	print('gid, egid', os.getgid(),os.getegid())
	input_data = input("Command String:")
	if(is_valid(input_data)):
		os.system(input_data) 
	else:
		print("Invalid!")
run()
