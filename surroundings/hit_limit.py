import os
import sys

'''
Goal: Predict the random random_numberber
How: Force the random random_numberber to be 4 by forcing an error.

Solution: 
- ulimit -n 5
- python3 hit_limit.py 2

'''
#os.system("ulimit -n 5") 

flag_contents = ""
with open('flag.txt') as f:
	flag_contents = f.read()

amount = input("Amount of files to read: ")
f_lst = []


for i in range(1,int(amount) + 1):
	f = open("files/" + str(i)) 
	f_lst.append(f)
	print(f.fileno()) 

def get_random():
	random_number = 0 

	# Geneate cookie
	try:
		f = open("/dev/random", 'rb')
		random_number = f.read(4)

	# Trigger too many open files error
	except OSError as err: # How can we make this fail?
		print(f"Unexpected {err=}, {type(err)=}")
		random_number = 4 # GOAL: Force this condition to occur.

	print("Random Number:", random_number)
	return random_number

random_number = get_random()
if(random_number == 4):
	print(flag_contents) 
else:
	print("Bad!")