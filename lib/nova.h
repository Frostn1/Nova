#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct link {
	char* name;
	char** expression;
	void** variables;

    (link*) new_link(char*, char**, void**);
    (void*) show_link(link*);
}link;

link* new_link(char* name_, char** expression_, void** variables_) {

}

void* show_link(link* link_) {
    
}
