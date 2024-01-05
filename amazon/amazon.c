#include <stdio.h> 
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>


// Given a directory, create an OTP value.
void create_otp(char* directory){

	// Get a random value between 0 and 9999
	int OTP = rand() % 10000;
	char OTP_string[8];
	char* string_ptr = malloc(32);

	// Convert from int to string. Keep leading 0's
	sprintf(OTP_string, "%04u", OTP); 
	
	// Setup the file creation string properly
	sprintf(string_ptr, "%s", directory); // copy directory into the string 
	strcat(string_ptr,"/"); // Add the slash between the values
	strcat(string_ptr, OTP_string); // Add the OTP value to the string

	// Create the file for the OTP token
	FILE *file_ptr = fopen(string_ptr, "w");
	fprintf(file_ptr, "%u", (int)time(NULL)); // Add the current time
	fclose(file_ptr);
	puts("Created OTP token");
	return; 
}

/*
Checks to see if an OTP sign in attempt is valid or not
Parameters: 
	directory: The location for the user 
	attempt: The OTP value
Returns: 
	0 for False and 1 for True
*/
int check_otp_attempt(char* directory, int attempt){

	// Iterate over all files in the users directory	
	DIR *dir_ptr = opendir(directory); 
	struct dirent *dir;
	unsigned int my_time; 
	time_t start_time = time(NULL);
	char* directory_full = malloc(100);

	if(!dir_ptr) return 0;

	// For each OTP entry, validate it and the time written.
	while((dir = readdir(dir_ptr)) != NULL){

		// If not a file, then move on 
		if(dir->d_type != DT_REG) continue; 
	
		// Create the string to read from the file
		sprintf(directory_full, "%s", directory);
		strcat(directory_full, "/");
		strcat(directory_full, dir->d_name);

		// Read the time from the file
		FILE * file_ptr = fopen(directory_full,"r");
		fscanf(file_ptr, "%u", &my_time);
		fclose(file_ptr);

		// The attempt matches the OTP token and was requested less than 3 minutes ago
		if(attempt == atoi(dir->d_name) && (start_time - 180) < my_time){
			free(directory_full);
			return 1; 
		}
	}

	free(directory_full);
	closedir(dir_ptr);
	puts("Failed attempt :(");
	return 0; 
}

/*
Sets up the random function.
Returns a pointer to a string
*/
char* setup(){
	
	// Randomly seed the random
	FILE* file_ptr = fopen("/dev/urandom", "r");
	int random_data; 	
	fread(&random_data, sizeof(random_data), 8, file_ptr);
	//fclose(file_ptr); <-- Crashes the program... Idk why

	srand(random_data);
	int setup_val = rand();
	//setup_val = 510936995;  <-- Tmp value

	// Create a directory with the random value
	char intro[] = "./OTP/";
	char directory[20];
	sprintf(directory, "%d", setup_val); //Convert integer to string

	// Create the directory
	char* full_directory = (char *) malloc(16);
	strcpy(full_directory, intro);
	strcat(full_directory, directory);
	
	// Is the directory previously existed, delete all contents :( 
	mkdir(full_directory, 0700);
	return full_directory;

}

int main(){
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stdin, NULL, _IONBF, 0);	
	char* directory = setup();	

	puts("Login complete. Entering the OTP login screen"); 
	
	int cont = 1;
	int option; 
	int result = 0;
	while(cont == 1){	
		puts("1. Create OTP code\n2. Check OTP code\n3. Exit");
		scanf("%d", &option);	
	
		// Create an OTP token	
		if(option == 1){
			create_otp(directory);
		}
		
		// Attempt an OTP token
		else if(option == 2){
			printf("Enter an OTP token: ");
			scanf("%d", &option);
			result = check_otp_attempt(directory,option);
			if(result == 1){ // Print the flag from a file
				FILE *fp; 
				int c; 
				fp = fopen("flag.txt","r");
				if(fp){
					while((c = getc(fp)) != EOF)
						putchar(c); 
					fclose(fp);
					return 0; 
			}
				puts("Flag....");
				// print flag :)
			return 0;
			}
		}
		
		// Quit
		else if(option == 3){
			return 0;
		}
	}
}
