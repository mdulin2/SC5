import os
import sys

'''
Goal: Predict the random number
How: Force the random number to be 4 by forcing an error.

Solution: 
- ulimit -n 5
- python3 hit_limit.py 2

'''
#os.system("ulimit -n 5") 

if(len(sys.argv) != 2):
	print("Hit limit without parameter")
	sys.exit(-1)

f_lst = []
for i in range(1,int(sys.argv[1]) + 1):
	f = open("files/" + str(i)) 
	f_lst.append(f)
	print(f.fileno()) 

def get_random():
	num = 0 

	# Geneate cookie
	try:
		f = open("/dev/random", 'rb')
		num = f.read(4)

	# Trigger too many open files error
	except OSError as err:
		print(f"Unexpected {err=}, {type(err)=}")
		num = 4
	print("Random Number:", num)
	return num

num = get_random()
if(num == 4):
	print("FLAG")
else:
	print("Bad!")
