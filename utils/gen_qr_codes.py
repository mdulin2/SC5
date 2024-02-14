import segno
import re
import os 
import random 

def checksum(string):
	d = 0
	for char in string:
	    d = d + ord(char)
	return d % 256

def read_file():
	f = open("student_data.csv")

	data = f.read()
	entries = data.split("\n")

	lst = []
	for entry in entries:
		lst.append(entry.split(","))
	
	return lst


# Get the list of teams 
team_lst = read_file()

if( not os.path.exists("teams/")):
	os.mkdir("teams/")

# Create the QR code for each of the teams
ticket_no = 0
for team in team_lst:
	if(team == [""]):
		continue

	base ="ZZZZZZZ|XXXXXXX|YYYYYYY|AAAAAAAAA|E|New York|Spokane|Delta|22C|"
	
	# For each team name, create a QR code
	name = team[0]
	team_name = team[1]

		# Truncate the name to prevent buffer overflows
	first = name.split(" ")[0][0:16]
	second = name.split(" ")[1][0:16]

	# Add the names to the string
	string = base.replace("XXXXXXX", first)
	string = string.replace("YYYYYYY", second)

	# Generate a random ticket number for their ticket
	flight_no = random.randint(10, 10000)

	string = string.replace("ZZZZZZZ", str(flight_no))


	# Craft the checksum for the final part of the challenge
	value = 0 # checksum(string)
	string_bck = ""
	while(value < 0x21 or value > 122):

		ticket_no = random.randint(100, 1000000)
		string_bck = string.replace("AAAAAAAAA", str(ticket_no))
		value = checksum(string_bck) 

	string = string_bck

	# Fix the team name to be valid for a file
	final_string = string + chr(value) + "|"
	print(final_string, value)
	team_name = re.sub('[^0-9a-zA-Z]+', '_', team_name)

	# Write the QR code
	qrcode = segno.make_qr(final_string) 
	qrcode.save("teams/{}.png".format(team_name) , scale=5) 

	# Now, do it again! :) 

