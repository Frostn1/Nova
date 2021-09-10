#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct link {
	char* name;
	char** expression;
	void** variables;
}link;
int main(int argc, char** argv) {
	int x = 1;
	link y = {"y", {"x", "+", "5"}, {&x, 0, 0}};
}