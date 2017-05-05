/*Dumb binary to modify system criticality.
 * */
#include "litmus.h"
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include "common.h"

int main(int argc, char* argv[]){
    
    int val = 0, fail;
    if(argc < 2){
        printf("Argument (Criticality) Missing.\n");
        return 0;
    }
    val = str2int(argv[1], &fail);
    printf("Value: %d\n", val);
    if(val <= 0){
        printf("Provide a valid criticality value in range 1-5\n");
        return 0;
    }

    if(set_system_criticality(val)){

    }
    return 1;
}

