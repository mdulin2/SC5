#include <stdlib.h>
#include <stdio.h>
#include <string.h>

/*
Compile: `gcc race_track.c -o race_track`

Env: 
- Should use GLibC 2.23
*/


// The main racer struct
struct racer {
	double points;
	long rank;
	char name[0x80];
};

// The main sponsor struct
struct sponsor {
	long usage_counter; 
	long last_grade;
	char name[32];
};

long sponsor_counter; // Counter for the amount of sponsors
struct racer* racers[16]; // List of racers 
int is_filled[16]; // Keeping track if a racer is in use or not

void* init(){
	puts("Greeings Ricky Bobby... You were born to race!"); 
	puts("Now, it is time to race and make all the money you can by getting the best sounding sponsors..."); 
	puts("Good luck!"); 

	// Initialize the global variables.
	sponsor_counter = 0;
	srand(time(0));
	
	// Disable stdout buffering
	setvbuf(stdout, NULL, _IONBF, 0);
}

/*
Creates a new racer in the next index. 
Returns 0 is this succeeded.
Returns 1 otherwise.
*/
int add_racer(){
	long index = 0;

	// Add to the closest 'free location'
	while(index < 16){
		if(is_filled[index] == 0){

			// Initialize the creation of the racer
			racers[index] = malloc(sizeof(struct racer));	
			memset(racers[index],0,sizeof(struct racer));
			
			is_filled[index] = 1; // Set the racer to be in use.

			printf("Enter the racer rank: ");
			scanf("%ld", &racers[index]->rank);		
			getchar(); // Eat the newline

			racers[index]->points = 0; // Initialize the player score

			printf("Enter the racers name: ");
			fgets(racers[index]->name, 32,stdin);
			return 0;
		}
		index += 1;	
	}	
	
	return 1;
}

// Print all available racers
void* list_racers(){
	int index = 0; 
	while(index < 16){
		if(is_filled[index] == 1){
			printf("Rank: %lu, Name: %s, Points: %lf", racers[index]->rank, racers[index]->name, racers[index]->points);
		}
		index += 1;
	}
}

// Print a specified racer
// Takes in the index as the racer to print.
void* view_racer(int index){
	if(index < 16 && index >= 0 && is_filled[index] == 1){
		printf("Rank: %lu, Name: %s, Points: %lf\n", racers[index]->rank, racers[index]->name, racers[index]->points);
	}else{
		puts("Invalid index!");
	}
}

// Given an index, it updates a racer.
int update_racer(int index){
	if(index < 16 && index >= 0 && racers[index] != 0){
		printf("Enter the racer rank: ");
		scanf("%lu", &racers[index]->rank);		
		getchar(); // Eat the newline

		// Update the racers name
		printf("Enter the racers name: ");
		fgets(racers[index]->name, 32,stdin);
		return 0;	
	}	
	printf("Invalid index... too large");
	
	return 1;
}

// Given an index, remove a racer
void* delete_racer(int index){
	if(index < 16 && is_filled[index] == 1 && index >= 0){
		free(racers[index]);
		is_filled[index] = 0;
		printf("Deleted index %d", index);

	}else{
		puts("Illegal index!");
	}
	
	return;
}

// Run the race! Takes in a sponsor struct as an arguement
long race(struct sponsor my_sponsor){
	
	// Get the racer to use
	int index; 
	printf("Enter the racer to use: ");
	scanf("%d", &index);
	getchar();
	if(index >= 16 || is_filled[index] != 1 && index >= 0){
		puts("Illegal racer! Don't cheat!");
		return -1; 
	}

	printf("Racing with %s, who is sponsored by %s", racers[index]->name, my_sponsor.name);
	
	// The race for the time
	double race_time = (double)rand()/(double)(RAND_MAX/10.0);	
	racers[index]->points = race_time;
	printf("\nYour time was %f!\n", race_time);

	// Get the sponsor feedback information
	unsigned long sponsor_grade; 
	printf("What rating would you give our sponsor?\n");
	scanf("%lu", &sponsor_grade);
	getchar();
	
	return sponsor_grade;
}

void* print_banner(){
	printf("\n\n=====================\n1. Create sponsor\n2. Print Sponsor Count \n3. List Sponsors\n4. View Sponsors\n5. Update sponsor\n6. Create a Racer\n7. List Racers\n8. View Racer\n9. Update Racer\n10. Delete Racer\n11. Race!\n12. Quit\n>");

}

int main(int argc, char *argv[]){
	init();
	// The array of sponsors
	struct sponsor sponsors[12];  		
	memset(sponsors, 0, sizeof(sponsors));

	// Variables for the program to run smoothly
	int is_cont = 1; 
	int option;
	int sub_option;
	while(is_cont){
		print_banner();
		scanf("%d", &option);
		getchar(); // Eat the newline
		
		// Add sponsor
		if(option == 1){
			if(sponsor_counter >= 12){
				puts("Too many sponsors!");
				continue;
			}
			printf("Enter your sponsor name: ");	
			fgets(sponsors[sponsor_counter].name, 32,stdin);

			sponsors[sponsor_counter].last_grade = 0; 
			sponsors[sponsor_counter].usage_counter = 0;
			sponsor_counter +=1;	

			puts("Thanks for sponsoring!");
			
		} 
		else if(option == 2){
			printf("Amount of sponsors: %lu\n", sponsor_counter);
		}
		// List sponsors
		else if(option == 3){
			for (int i = 0; i < sponsor_counter; i++){
				printf("Sponsor %d: %s\n", i + 1, sponsors[i].name);
			}
		}
	
		// View sponsors	
		else if(option == 4){
			printf("Enter an index to view: ");
			scanf("%d", &sub_option);
			getchar(); // Eat the newline

			if(sub_option >= 0 && sub_option <= sponsor_counter - 1 && sponsor_counter != 12){
				printf("Sponsor %s -- Uses: %lu, Last Score: %lu \n",  sponsors[sub_option].name, sponsors[sub_option].usage_counter, sponsors[sub_option].last_grade);
			}else{
				puts("Illegal Index!");
			}
		}
		// Update sponsors 
		else if(option == 5){
			printf("Enter an index to update: ");
			scanf("%d", &sub_option);
			getchar(); // Eat the newline		
			
			if(sub_option < 0 || sub_option > sponsor_counter -1){
				printf("Illegal index!");
				continue;
			}
			puts("Giving the sponsor a clean slat....");

			// Edit sponsor name
                        printf("Enter your sponsor name: ");
                        fgets(sponsors[sub_option].name, 32,stdin);		
			sponsors[sub_option].last_grade = 0; 
			sponsors[sub_option].usage_counter = 0;
		}
		
		// Add racer
		else if(option == 6){
			add_racer();
		}	
		// List racers
		else if(option == 7){
			list_racers();
		}

		// View racer	
		else if(option == 8){
			puts("Enter the index to view: ");
			scanf("%d", &sub_option);
			getchar(); // Eat the newline		
	
			view_racer(sub_option);
		}
		// Update racer 
		else if(option == 9){
			puts("Enter the index to update: ");
			scanf("%d", &sub_option);
			getchar();

			update_racer(sub_option);
		}

		// Delete racer 		
		else if(option == 10){
			printf("Enter the index to delete: ");
			scanf("%d", &sub_option);
			getchar();

			delete_racer(sub_option);
		}
		else if(option == 11){
			printf("Enter in the sponsor to use: ");
			scanf("%d", &sub_option);
			getchar();

			if(sub_option > sponsor_counter - 1){
				puts("Invalid sponsor index!");
				continue;
			}
			// Get sponsor information. Pass in the sponsor as input.
			// Return the grade for the sponsor
			sponsors[sub_option].last_grade = race(sponsors[sub_option]);
			// Update the usage of the sponsor
			sponsors[sub_option].usage_counter += 1;
		}
		// Quit....
		else if(option == 12 ){
			is_cont = 0;
		}

	}	

	return 0;
}

