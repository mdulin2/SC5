#include <stdio.h>
#include <stdlib.h> 
#include <string.h>
#include <strings.h>
#include <linux/limits.h>

/*
Compile: 
- gcc error_code.c -o error_code
*/

// In particular, disallow semicolons, backticks, single quotes, dollar signs and other shell characters. 
// Only allows alphanumeric, parens, single/double quotes and backslashes
char* white_lst = "abcdefghijklmnopqrstuvwxyz'1234567890#\"\\ .";
//char *white_lst = "abcdefghijklmnopqrstuvwxyz'1234567890# .\\\"()";
/*
Ensure that all characters in the string are in the whitelisted character sheet 
Returns 0 for false and 1 for true.
*/
int is_valid_chars(char* str){
	int pass = 0;
	for (int i=0; i < strlen(str); i++){
		pass = 0;
		for (int j=0; j < strlen(white_lst); j++){
			
			if(str[i] == white_lst[j]){
				pass = 1; 
			}
		}
		if(pass == 0){
			printf("Invalid character: %c\n", str[i]);
			return 0; 
		}
	}
	return 1;

} 

int validate_file(char* filename){
	char actualpath [PATH_MAX+1];
	char* ptr; 

	// Get the absolute path
	ptr = realpath(filename, actualpath);

	if(ptr == NULL){
		puts("Error occured on path resolution");
		return 0;
	}

	// Validate the file name
	if(strstr(actualpath, "flag") != NULL){
		puts("Flag cannot be in the file name");
		return 0;
	}
	if(strstr(actualpath, "etc") != NULL){
		puts("etc cannot be in the file name");
		return 0;
	}

	return 1;
}

/*
Takes two parameters as input: the file name and the code type. 
*/
int main(int argc, char* argv[]){


	if(argc != 3){
		puts("./error_code <file_name> <code_type>"); 
		return 1;
	}

	// Copy arguement 1 into a buffer
	char* file = malloc(strlen(argv[1])); 
	strncpy(file, argv[1], strlen(argv[1]) +1);

	// Validate parameters 1 and 2 
	if(!is_valid_chars(file)){
		printf("Please select from the valid character set: %s\n", white_lst); 
		return 0; 
	}

	/*
	// Validate that the file is NOT the flag
	if(!validate_file(file)){
		return 0; 		
	}
	*/
	// validate that perl, gcc or python is being used
	if(strcmp(argv[2], "perl") != 0 && strcmp(argv[2], "python") != 0 && strcmp(argv[2], "php") != 0){
		puts("Select from the following programs: perl, python and gcc"); 	
		return 1; 
	}
	
	// The main command being ran 	
	char* command1 = "tcpdump -d -r"; 
	// Get the output from stderr and redirect it. 
	char* command2 = "2>&1 >/dev/null |"; 

	// Calculate the size of the buffer. We add an extra 5 because of the spaces and double quotes in the snprintf used below.
	int command_size = strlen(command1) + strlen(file) + strlen(command2) + strlen(argv[2]) + 6; 
	char* full_command = malloc(command_size); 

	// Concatenates the string to create the OS command using snprintf
	snprintf(full_command, command_size, "%s \"%s\" %s %s", command1, file, command2, argv[2]);
	puts(full_command); 

	// Execute the command 
	system(full_command); 
	return 0; 
}
