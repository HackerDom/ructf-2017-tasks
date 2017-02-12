#include <stdio.h>
#include <string.h>
#include <stdlib.h>


#define TRUE "True"
#define FALSE "False"
#define FLAG_HASH "LQRHQTIOENUDHSFAWCBWKLUVBHAGXMHFNFHGAWXGKIBOSVNPGWIOVPDLVMXCXHIC"
#define LEN 64
#define byte unsigned char


inline void swap(byte* a, byte* b)
{
	*a = *a ^ *b;
	*b = *a ^ *b;
	*a = *b ^ *a;
}

void bwt(size_t length, char* input)
{
	char* buffer = malloc(length << 1);
	strncpy(buffer, input, length);
	strncpy(buffer + length, input, length - 1); // The program will crash if length == 0
	byte* sorted = malloc(length);
	for (size_t i = 0; i < length; i++)
		sorted[i] = i;

	for (size_t i = 0; i < length; i++)
		for (size_t j = length - 1; j > i; j--)
			if (strncmp(buffer + sorted[j - 1], buffer + sorted[j], length) > 0)
				swap(&sorted[j - 1], &sorted[j]);

	for (size_t i = 0; i < length; i++)
		input[i] = buffer[sorted[i] + length - 1];

	free(sorted);
	free(buffer);
}

void task(byte length)
{
	char input[LEN];
	scanf("%s", input);
	byte factual_length = strlen(input);
	if (factual_length == length)
	{
		bwt(factual_length, input);
		printf(strncmp(FLAG_HASH, input, length) == 0 ? TRUE : FALSE);
		goto end;
	}
	printf(FALSE);
end:
	fflush(stdout);
	exit(0);
}

int main()
{
	task(LEN);
	return 0;
}
