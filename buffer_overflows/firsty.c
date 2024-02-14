#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <pwd.h>

/*
Compile: 
`gcc -z execstack -m32 firsty.c -fno-stack-protector -o firsty -no-pie`
*/

// Below function declarations
uid_t get_priv_uuid(); 
void setup_permissions(); 
void setup(); 

struct danger {
	char my_string[32];
	unsigned int special_int; // Corrupt Me!
}; 

void print_flag(){
    puts("Congrats! ;)");

    FILE *fp; 
    int c; 
    fp = fopen("flag.txt","r");

    // Read the output of the flag file    
    if(fp){
        while((c = getc(fp)) != EOF)
            putchar(c); 
        fclose(fp);

    }else {
          puts("Unable to read flag");
    }
}


int main(){

	// Ignore this function...
	setup(); 


	// Create a local variable on the stack 
	struct danger my_data; // Location to overwite.
	
	// Set my cool variable 
	my_data.special_int = 0x11223344;
	
	// Put data into my cool string 
	printf("Please insert a cool string: ");
	fgets(my_data.my_string,0x100,stdin);

	if(my_data.special_int != 0x11223344){
		print_flag();
	}
	else{
		puts("Lit :fire");
	}
	return 0;
}













///////////////////////////////////
/// Ignore everything below here
///////////////////////////////////
void setup(){
	// Ignore this...
	setup_permissions();  

	// Ignore this...
	setvbuf(stdout, NULL, _IONBF, 0);
}

// Get the uid of the 'execStackPriv'
uid_t get_priv_uuid(){
   	struct passwd pwd;
    struct passwd *result;
    char *buf;
    size_t bufsize;
    int s;

   	bufsize = sysconf(_SC_GETPW_R_SIZE_MAX);
    if (bufsize == -1)          /* Value was indeterminate */
        bufsize = 16384;        /* Should be more than enough */

   	buf = malloc(bufsize);
    if (buf == NULL) {
        perror("malloc");
        exit(EXIT_FAILURE);
    }

	// User we're trying to elevate too.
   	s = getpwnam_r("firstyPriv", &pwd, buf, bufsize, &result);
    if (result == NULL) {
        if (s == 0)
            printf("Not found\n");
        else {
            errno = s;
            perror("getpwnam_r");
        }
        exit(EXIT_FAILURE);
    }

	return pwd.pw_uid;
}

// Sets the permissions to that of the 'execStack' priv user.
void setup_permissions(){ // Ignore this...

	// Ignore...
	setvbuf(stdout, NULL, _IONBF, 0);
	
	uid_t user = get_priv_uuid(); // User we WANT to execute as
	uid_t current_user = getuid(); // User we CURRENTLY are executing as

	// If we aren't the 'user' at this point, then skip this code.
	// Necessary for debuggers to call this and not crash.
	if(current_user == 1000 && geteuid() == 1000){
		return; 
	}

	// Set the group id of the process
	int error = setgid(user);
	if(error < 0){
		puts("setgid error");
        exit(EXIT_FAILURE);		
	}
	error = setegid(user);
	if(error < 0){
		puts("Setegid error");
        exit(EXIT_FAILURE);		
	}
	error = setuid(user);
	if(error < 0){
		puts("Seteuid error");
        exit(EXIT_FAILURE);		
	}
	error = seteuid(user);
	if(error < 0){
		puts("Seteuid error");
        exit(EXIT_FAILURE);		
	}
}
