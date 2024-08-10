#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "khash.h"
#include <ctype.h>

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

typedef struct vcfLine{
    char* chromNum;
    char* startPos;
    char* endPos;
    int mutatedPos;
    char* id;
    char* refGene;
    char* altGenes;
    char* qual;
    char* filter;
    char* info;

} vcfLine;

vcfLine** getVCFLines(chrome2yourdome** sequences, int lineCount){
    // printf("------------------------------------------\n");
    long numVCFLines = 0;
    for (int i = 0; i < lineCount/2; i++){
        numVCFLines += strlen(sequences[i]->sequenceData); 
    }

    int index = 0;
    vcfLine** lines = malloc(numVCFLines * sizeof(vcfLine*));
    for (int i = 0; i < lineCount/2; i++){
        char* input = strtok(sequences[i]->chromAnnot, ">");
        char* cNumber = strtok(strdup(input), ":");
        char* inter = strtok(NULL, "");
        char* sPos = strtok(inter, "-");
        char* ePos = strtok(NULL, "-");

        for (int j = 0; j < strlen(sequences[i]->sequenceData); j++){
            lines[index] = malloc(sizeof(vcfLine));
            lines[index]->chromNum = malloc(10 * sizeof(char) + 1);
            lines[index]->startPos = malloc(10 * sizeof(char) + 1);
            lines[index]->endPos = malloc(10 * sizeof(char) + 1);
            // lines[index]->mutatedPos = malloc(sizeof(int));
            lines[index]->id = malloc(sizeof(char*) + 1);
            lines[index]->refGene = malloc(sizeof(char) + 1);
            lines[index]->altGenes = malloc(3 * sizeof(char) + 1);
            lines[index]->qual = malloc(sizeof(char*) + 1);
            lines[index]->filter = malloc(sizeof(char*) + 1);
            lines[index]->info = malloc(sizeof(char*) * 20);

            lines[index]->id = ".";
            lines[index]->qual = ".";
            lines[index]->filter = ".";
            lines[index]->info = ".";

            strcpy(lines[index]->chromNum, cNumber);
            strcpy(lines[index]->startPos, sPos);
            strcpy(lines[index]->endPos, ePos);
            lines[index]->mutatedPos = j + atoi(sPos);

            char rGene = toupper(sequences[i]->sequenceData[j]);
            char* rGeneString = malloc(2 * sizeof(char));
            rGeneString[0] = rGene;
            rGeneString[1] = '\0';

            char* altGeneString;
            if (strcmp(rGeneString, "A") == 0){
                altGeneString = "CGT";
            }
            else if (strcmp(rGeneString, "C") == 0){
                altGeneString = "AGT";
            }
            else if (strcmp(rGeneString, "G") == 0){
                altGeneString = "ACT";
            }
            else if (strcmp(rGeneString, "T") == 0){
                altGeneString = "ACG";
            }

            strcpy(lines[index]->refGene, rGeneString);
            strcpy(lines[index]->altGenes, altGeneString);

            index += 1;
        }
    }

    return lines;
}

int getLineLength(vcfLine * line){
    return strlen(line->chromNum) + 1 + strlen(line->refGene) + strlen(line->altGenes) + strlen(line->qual) + strlen(line->filter) + strlen(line->info);
}

char* getTableLine(vcfLine* line){
    // fprintf(file, "%s\t%d\t%s\t%c\t%s\t%s\n")
    char* lineString1 = malloc(sizeof(char*) * getLineLength(line));
    char* lineString2 = malloc(sizeof(char*) * getLineLength(line));
    char* lineString3 = malloc(sizeof(char*) * getLineLength(line));
    char* finalLine = malloc(3 * sizeof(char*) * getLineLength(line));

    sprintf(lineString1, "%s\t%d\t%s\t%s\t%c\t%s\t%s\t%s", 
        line->chromNum, line->mutatedPos, line->id, line->refGene, line->altGenes[0], line->qual, line->filter, line->info);
    sprintf(lineString2, "%s\t%d\t%s\t%s\t%c\t%s\t%s\t%s", 
        line->chromNum, line->mutatedPos, line->id, line->refGene, line->altGenes[1], line->qual, line->filter, line->info);
    sprintf(lineString3, "%s\t%d\t%s\t%s\t%c\t%s\t%s\t%s", 
        line->chromNum, line->mutatedPos, line->id, line->refGene, line->altGenes[2], line->qual, line->filter, line->info);

    sprintf(finalLine, "%s\n%s\n%s\n", lineString1, lineString2, lineString3);

    return finalLine;
}

int main(int argc, char** argv){
    // INFERENCE COMMAND ==> insilico_mutator *fasta filepath* *output vcf filepath*
    printf("Extractin Fasta Data ==> %s\n", argv[1]);
    printf("Transforming into VCF ==> %s\n", argv[2]);
    char* filePath = argv[1];
    char* fileData = getFileData(filePath);

    int lineCount = 0;
    for (int i = 0; i < strlen(fileData); i++){
        if (fileData[i] == '\n'){
            lineCount++;
        }
    }

    chrome2yourdome** sequences = populateStructs(fileData);
    /*
    printf("------------------------------------------\n");
    for (int i = 0; i < (int) lineCount/2; i++){
        printf("CHR ANNOT | %s\n", sequences[i]->chromAnnot);
        printf("SEQUENCE  | %li\n", strlen(sequences[i]->sequenceData));
        printf("------------------------------------------\n");
    }
    */

    FILE* file;
    file = fopen(argv[2], "w");

    fprintf(file, "##fileformat=VCFv4.2\n");
    fprintf(file, "##source=InSilicoMutatorV2\n");
    fprintf(file, "##reference=../fasta_data/hg38.fa\n");
    fprintf(file, "##INFO=<ID=Undefined,Number=Undefined,Type=Undefined,Description=Undefined>\n");
    fprintf(file, "##INFO=<ID=Undefined,Number=Undefined,Type=Undefined,Description=Undefined>\n");
    fprintf(file, "##INFO=<ID=Undefined,Number=Undefined,Type=Undefined,Description=Undefined>\n");
    fprintf(file, "##FILTER=<ID=Undefined,Description=Undefined\n");
    fprintf(file, "##FILTER=<ID=Undefined,Description=Undefined\n");

    fprintf(file, "#CHROM\tPOS\t\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n");
    long size = 0;
    vcfLine** lines = getVCFLines(sequences, lineCount);
    for (int i = 0; lines[i] != NULL; i++){
        vcfLine* line = lines[i];

        fprintf(file, "%s", getTableLine(line));
        /*
        fprintf(file, "%s\t%d\t%s\t%c\t%s\t%s\n", 
            line->chromNum, line->mutatedPos, line->refGene, line->altGenes[1]);
        fprintf(file, "%s\t%d\t%s\t%c\t%s\t%s\n", 
            line->chromNum, line->mutatedPos, line->refGene, line->altGenes[2]);
        */

        size++;
    }

    fclose(file);

    return 0;
}
