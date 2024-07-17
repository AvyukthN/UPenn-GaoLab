#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* getFileData(char* filePath){
    FILE* filePtr;

    filePtr = fopen(filePath, "r");

    // int fseek(FILE* stream, long int number of bytes to move file pointer (can be +, -, or 0), int position from which to calculate offset);
    // first call to fseek moves the filePtr to the end of the file telling and ftell returns the current position of the pointer which gives us the total size of the file in bytes
    // the second call to fseek moves the pointer back to the beginning of the file
    fseek(filePtr, 0, SEEK_END);
    long fileSize = ftell(filePtr);
    fseek(filePtr, 0, SEEK_SET);

    // we use the fileSize calculated before to allocate an accurate amount of memory into the fileData buffer
    // the plus 1 is added so we can append the null terminator at the end of the string we read in
    char* fileData = malloc(fileSize + 1);
    if (fileData == NULL){
        fclose(filePtr);
        return "MEMORY ALLOCATION FAILED CHECK FILE\n";
    }

    // fread(buffer where data from file will be stored, each elements size in bytes, number of elements to read (file size), the file pointer to read from);
    long readSize = fread(fileData, 1, fileSize, filePtr);
    if (readSize != fileSize){
        free(fileData);
        fclose(filePtr);
        return "ERROR READING FILE\n";
    }

    // adding null terminator to the end of the string data read in from the file
    fileData[fileSize] = '\0';
    fclose(filePtr);

    return fileData;
}

typedef struct chrome2yourdome{
    char* chromAnnot;
    char* sequenceData;

} chrome2yourdome;

chrome2yourdome** populateStructs(char* fileData){
    int lineCount = 0;
    for (int i = 0; i < strlen(fileData); i++){
        if (fileData[i] == '\n'){
            lineCount++;
        }
    }

    chrome2yourdome** sequences = malloc(lineCount * sizeof(chrome2yourdome*));
    int seqsRead = 0;

    char* line = strtok(fileData, "\n");
    while (line != NULL && seqsRead < lineCount){
        if (line[0] == '>'){
            sequences[seqsRead] = malloc(sizeof(chrome2yourdome));
            sequences[seqsRead]->chromAnnot = malloc((strlen(line) * sizeof(char)) + 1);
            // sequences[seqsRead]->chromAnnot = malloc((strlen(line) * sizeof(char)) + 1);
            strcpy(sequences[seqsRead]->chromAnnot, line);
            // sequences[seqsRead]->chromAnnot = realloc(sequences[seqsRead]->chromAnnot, strlen(line) + 1);
            sequences[seqsRead]->chromAnnot[strlen(line)] = '\0';


            line = strtok(NULL, "\n");
            if (line != NULL){
                // sequences[seqsRead] = malloc(sizeof(chrome2yourdome));
                sequences[seqsRead]->sequenceData = malloc((strlen(line) * sizeof(char)) + 1);
                // sequences[seqsRead]->sequenceData = malloc((strlen(line) * sizeof(char)) + 1);
                strcpy(sequences[seqsRead]->sequenceData, line);
                sequences[seqsRead]->sequenceData[strlen(line)] = '\0';

                seqsRead++;
            }
        }

        line = strtok(NULL, "\n");
    }

    return sequences;
}

int main(){
    char* filePath = "./BRCA2_hg38_extracted.txt";
    char* fileData = getFileData(filePath);

    int lineCount = 0;
    for (int i = 0; i < strlen(fileData); i++){
        if (fileData[i] == '\n'){
            lineCount++;
        }
    }

    chrome2yourdome** sequences = populateStructs(fileData);

    printf("------------------------------------------\n");
    for (int i = 0; i < (int) lineCount/2; i++){
        printf("CHR ANNOT | %s\n", sequences[i]->chromAnnot);
        printf("SEQUENCE  | %li\n", strlen(sequences[i]->sequenceData));
        printf("------------------------------------------\n");
    }

    return 0;
}
