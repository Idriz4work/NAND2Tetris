#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct
{
	char* name;
	int num;
	char loop;
	int isA;
	int isC;
} symbol;

typedef struct
{
	char dest;
	char comp;
	char jump;
} Cinstruction;



int main()
{
	FILE *file = open(".asm",wor_ONLY);
	FILE *destfile = open(".hack",wor_ONLY);
	
}

int predefined()
{

}

int variables()
{

}

int labeled()
{

}



