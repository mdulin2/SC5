#include <pwd.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

// Get the uid of the 'flag_user'
uid_t get_uid(){
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

   	s = getpwnam_r("flag_user", &pwd, buf, bufsize, &result);
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

// Sets the permissions to that of the 'flag_user' user.
void setup_permissions(){
	uid_t user = get_uid();
	printf("UID: %u\n", user);

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
	// Set the user ID of the process. Order IS important between user and group.
	error = setuid(user);
	if(error < 0){
		puts("Setuid error");
        exit(EXIT_FAILURE);		
	}

	error = seteuid(user);
	if(error < 0){
		puts("Seteuid error");
        exit(EXIT_FAILURE);		
	}
}

void setup_env(){

	// Remove malicious ENV variables that would be inheritted by the process
	clearenv();

	// Add the PATH make in
	putenv("PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin");
}

int main(int argc, char *argv[])
{
	setup_permissions();
	setup_env();
	system("/usr/bin/python /home/odd/odd.py");
}
