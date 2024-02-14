def write_for_qr(teams):
        lines = []
        for team in teams:
                line = ""
                info = teams[team]
                line = info[0][0] + " " + info[0][1] + "," + team

                lines.append(line)

        f = open("student_data.csv", "a")
        f.write("\n".join(lines))
        f.close()

def read_file():
	f = open("d.txt", "r")
	data = f.read()
	
	data = data.split("\n")
	teams = []
	team = []
	state = 0
	for line in data:
		if(len(line) == 0):
			continue

		if(line[0] != "-"):
			continue 

		if(line[1] == "-"):
			if(state == 1):
				state = 0
				teams.append(team)
				print(team)
				team = []
			elif(state == 0):
				state = 1
			continue
	
		team.append(line.split(" ")[1:3])	
	
	for team in teams: 
		my_team = team
		player = " ".join(my_team[0])
		print(player) 

read_file()

