/*
gcc -mpreferred-stack-boundary=2 -m32 -ggdb -g -fno-stack-protector auth.c -o auth -no-pie

Ensure that ASLR is turned off for this challenge.
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int validate_serial(){
    printf("Enter a serial to login: \n");
    char serial[16];
    fscanf(stdin, "%s", serial);
    return 0;
}

// How to get to this point if validate_serial always returns false!?
int do_valid_stuff(){
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

int main( int argc, char *argv[]){
    if(validate_serial()){
        do_valid_stuff();
    }
    else{
        printf("Invalid serial number!\n");
    }
}
