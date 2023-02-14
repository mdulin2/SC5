
def get_lst():
	word_dict = {}
	word_lst_fd = open("words.txt", "r")
	index = 0
	for line in word_lst_fd: 
		line = line.replace('\n','') 
		line = line.replace(' ', '') 
		word_dict[index] = line
		index += 1

	return word_dict

def encode(key): 
	word_lst = get_lst()

	print(key) 
	passphrase = ""	

	print("Convert key to passphrase")
	while(key != 0):
		passphrase += word_lst[key % 32] + '-'
		key = key/32  # 32 words in the word list. Make this a base32 value

	passphrase = passphrase[:-1]
	return passphrase
		
# hallucinate-cat-victory-people-barley-giddy-kangaroo-yank
