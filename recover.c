#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

bool is_start_of_jpeg(BYTE buffer[]);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover FILE\n");
        return 1;
    }

    FILE *card = fopen(argv[1], "rb");
    if (card == NULL)
    {
        printf("Could not open the memory card.\n");
        return 2;
    }

    uint8_t buffer[BLOCK_SIZE];

    FILE *outfile = NULL;
    char filename[8];
    int n = 0;
    bool is_jpeg = false;

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        if (is_start_of_jpeg(buffer))
        {
            if (is_jpeg)
                fclose(outfile);

            sprintf(filename, "%03i.jpg", n);
            outfile = fopen(filename, "wb");
            if (outfile == NULL)
            {
                printf("Could not create output file %s\n", filename);
                return 1;
            }
            is_jpeg = true;
            n++;
        }

        if (is_jpeg)
        {
            fwrite(buffer, sizeof(BYTE), BLOCK_SIZE, outfile);
        }
    }
    if (outfile != NULL)
    {
        fclose(outfile);
    }

    fclose(card);
    return 0;
}

bool is_start_of_jpeg(BYTE buffer[])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && buffer[3] >= 0xe0 &&
           buffer[3] <= 0xef;
}
