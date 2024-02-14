
import re 

file = open("/5th Annual Spokane Cyber Cup Registration .csv", "r")
content = file.read().split("\n")[1:]
team_count = 0
individual_count = 0

form_index = 0
volunteers = {}
students = {}
individuals = {}
teams = {}
dups = 0
#content = content[78:]

for entry in content:
	entry = entry.replace('"', "").split(",")
	page_type = entry[1]

	if(page_type == 'Volunteer Registration'):
		firstname = entry[2]
		lastname = entry[3]
		email = entry[4]
		volunteers[firstname + " " + lastname] = [firstname, lastname, email]
	elif(page_type == "Single Participant Registration"):
		firstname = entry[7].replace(" ", "").lower()
		lastname = entry[8].replace(" ", "").lower()
		email = entry[9]
		school = entry[12].lower()
		grade = entry[13].lower()
		individual_count += 1

		if((firstname + " " + lastname) in students):
			print(firstname,lastname) 
			dups += 1
		students[firstname + " " + lastname] = [firstname, lastname, email, school, grade]

		individuals[firstname + " " + lastname] = [firstname, lastname, email, school, grade]
		#print(firstname, lastname, email, school, grade)

	elif(page_type == "Team Registration"):
		teamname = entry[16]
		team_count += 1

		team_list = []

		# Find the emails then trace where we want to get the data. Only reliable way to do it sadly.
		for i in range(17, len(entry)):
			elt = entry[i]
			email_validate_pattern = r"^\S+@\S+\.\S+$"
			email_count = re.match(email_validate_pattern, elt) 
			if(email_count != None):
				email = elt 
				name = entry[i-2].replace(" ","").lower() + " " + entry[i-1].replace(" ","").lower()
				if(entry[i+2] == "University" or entry[i+2] == "High School"):
					school = entry[i+3].lower()
				else:
					school = entry[i+2].lower()
				shirt = entry[i+1]
				grade = entry[i+4].lower()

				if(name in students):
					print(name)
					dups += 1

				students[name] = [name.split(" ")[0], name.split(" ")[1], email, school, grade, teamname]

				team_list.append([name.split(" ")[0], name.split(" ")[1], email, school, grade])

		if(teamname in teams):
			print("Dup on team!")
			#print(name, email, grade, school, shirt) 
			
		teams[teamname] = team_list
	form_index += 1

def write_for_qr(teams):
	lines = []
	for team in teams: 	
		line = ""
		info = teams[team]
		line = info[0][0] + " " + info[0][1] + "," + team 

		lines.append(line) 
	
	f = open("student_data.csv", "w")
	f.write("\n".join(lines))
	f.close()

print("Student count: ", len(students))
print("Individual count:", individual_count, individual_count/3)
print("Team count: ", len(teams))
print("Dups:", dups)

write_for_qr(teams) 

years = {}
schools = {}
for student in students:
	values = students[student]
	'''
	if(len(values) == 6):
		print("{},{},{},{},{}".format(student, values[2], values[3], values[4], values[5]))
	else:
	
		print("{},{},{},{},".format(student, values[2], values[3], values[4]))
	'''
	year = values[4]
	if(year not in years):
		years[year] = 1 
	else: 
		years[year] += 1

	school = values[3]
	if(school not in schools):
		schools[school] = 1 
	else: 
		schools[school] += 1

#print(schools) 
print(teams) 
#print(volunteers) 
