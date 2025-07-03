#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define BLOCK_SIZE 512

typedef uint8_t BYTE;

// File signatures
bool is_start_of_jpeg(BYTE buffer[]);
bool is_start_of_png(BYTE buffer[]);
bool is_start_of_pdf(BYTE buffer[]);
bool is_start_of_docx(BYTE buffer[]);
bool is_start_of_gif(BYTE buffer[]);
bool is_start_of_mp3(BYTE buffer[]);
bool is_start_of_bmp(BYTE buffer[]);
bool is_start_of_rar(BYTE buffer[]);

// File type enumeration
typedef enum {
    TYPE_UNKNOWN = 0,
    TYPE_JPEG,
    TYPE_PNG,
    TYPE_PDF,
    TYPE_DOCX,
    TYPE_GIF,
    TYPE_MP3,
    TYPE_BMP,
    TYPE_RAR
} FileType;

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
    char filename[12]; // Increased size for longer extensions
    int n = 0;
    FileType current_type = TYPE_UNKNOWN;
    bool file_open = false;

    while (fread(buffer, sizeof(BYTE), BLOCK_SIZE, card) == BLOCK_SIZE)
    {
        FileType detected_type = TYPE_UNKNOWN;
        
        // Check for file signatures
        if (is_start_of_jpeg(buffer))
            detected_type = TYPE_JPEG;
        else if (is_start_of_png(buffer))
            detected_type = TYPE_PNG;
        else if (is_start_of_pdf(buffer))
            detected_type = TYPE_PDF;
        else if (is_start_of_docx(buffer))
            detected_type = TYPE_DOCX;
        else if (is_start_of_gif(buffer))
            detected_type = TYPE_GIF;
        else if (is_start_of_mp3(buffer))
            detected_type = TYPE_MP3;
        else if (is_start_of_bmp(buffer))
            detected_type = TYPE_BMP;
        else if (is_start_of_rar(buffer))
            detected_type = TYPE_RAR;
        
        // If we found a new file signature
        if (detected_type != TYPE_UNKNOWN)
        {
            // Close previous file if one was open
            if (file_open && outfile != NULL)
                fclose(outfile);
            
            // Create filename with appropriate extension
            switch (detected_type)
            {
                case TYPE_JPEG:
                    sprintf(filename, "%03i.jpg", n);
                    break;
                case TYPE_PNG:
                    sprintf(filename, "%03i.png", n);
                    break;
                case TYPE_PDF:
                    sprintf(filename, "%03i.pdf", n);
                    break;
                case TYPE_DOCX:
                    sprintf(filename, "%03i.docx", n);
                    break;
                case TYPE_GIF:
                    sprintf(filename, "%03i.gif", n);
                    break;
                case TYPE_MP3:
                    sprintf(filename, "%03i.mp3", n);
                    break;
                case TYPE_BMP:
                    sprintf(filename, "%03i.bmp", n);
                    break;
                case TYPE_RAR:
                    sprintf(filename, "%03i.rar", n);
                    break;
                default:
                    break;
            }
            
            // Open new file
            outfile = fopen(filename, "wb");
            if (outfile == NULL)
            {
                printf("Could not create output file %s\n", filename);
                return 1;
            }
            
            current_type = detected_type;
            file_open = true;
            n++;
            printf("Recovering file: %s\n", filename);
        }

        // Write to file if one is open
        if (file_open && outfile != NULL)
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

bool is_start_of_png(BYTE buffer[])
{
    // PNG signature: 89 50 4E 47 0D 0A 1A 0A
    BYTE png_sig[] = {0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A};
    return memcmp(buffer, png_sig, 8) == 0;
}

bool is_start_of_pdf(BYTE buffer[])
{
    // PDF signature: 25 50 44 46 ("%PDF")
    return buffer[0] == 0x25 && buffer[1] == 0x50 && buffer[2] == 0x44 && buffer[3] == 0x46;
}

bool is_start_of_docx(BYTE buffer[])
{
    // DOCX (ZIP) signature: 50 4B 03 04
    return buffer[0] == 0x50 && buffer[1] == 0x4B && buffer[2] == 0x03 && buffer[3] == 0x04;
}

bool is_start_of_gif(BYTE buffer[])
{
    // GIF signature: 47 49 46 38 37/39 61 (GIF87a/GIF89a)
    return buffer[0] == 0x47 && buffer[1] == 0x49 && buffer[2] == 0x46 && buffer[3] == 0x38 &&
           (buffer[4] == 0x37 || buffer[4] == 0x39) && buffer[5] == 0x61;
}

bool is_start_of_mp3(BYTE buffer[])
{
    // MP3 signature: ID3 (49 44 33) or MPEG frame sync (FF FB)
    return (buffer[0] == 0x49 && buffer[1] == 0x44 && buffer[2] == 0x33) || 
           (buffer[0] == 0xFF && buffer[1] == 0xFB);
}

bool is_start_of_bmp(BYTE buffer[])
{
    // BMP signature: 42 4D (BM)
    return buffer[0] == 0x42 && buffer[1] == 0x4D;
}

bool is_start_of_rar(BYTE buffer[])
{
    // RAR signature: 52 61 72 21 1A 07
    return buffer[0] == 0x52 && buffer[1] == 0x61 && buffer[2] == 0x72 && 
           buffer[3] == 0x21 && buffer[4] == 0x1A && buffer[5] == 0x07;
}
