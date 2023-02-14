
def get_lst():
	print("Import dictionary...")
	word_dict = {}
	word_lst_fd = open("words.txt", "r")
	index = 0
	for line in word_lst_fd: 
		line = line.replace('\n','') 
		line = line.replace(' ', '') 
		word_dict[line] = index
		index += 1

	return word_dict

def decode(passphrase): 
	word_lst = get_lst()

	print("Map passphrase to index and numerical value")
	index = 0
	my_key = 0
	passphrase = passphrase.split("-")
	for key in passphrase:

		# Get the word associated with the index
		pos = word_lst[key]

		# Each index is to the base of 32 * the index to get the original value.
		my_key = pos * 32 ** index + my_key
		index += 1
		
	return my_key
		
phrase = "hallucinate-cat-victory-people-barley-giddy-kangaroo-yank"
print(decode(phrase)) 
print("Convert the above value to be in base 32.")
