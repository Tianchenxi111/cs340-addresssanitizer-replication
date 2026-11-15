/* Original teaching cases for this replication; intentionally contains UB. */
#include <stdlib.h>
#include <string.h>

static volatile unsigned char global_data[16];
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    volatile unsigned char stack_data[16] = {0};
    volatile unsigned char *heap = malloc(16);
    if (!heap) return 3;
    heap[0] = 42;
    volatile int index = 16;
    if (!strcmp(argv[1], "heap")) heap[index] = 1;
    else if (!strcmp(argv[1], "stack")) stack_data[index] = 1;
    else if (!strcmp(argv[1], "global")) global_data[index] = 1;
    else if (!strcmp(argv[1], "uaf")) { free((void *)heap); return heap[0]; }
    else if (strcmp(argv[1], "clean")) { free((void *)heap); return 2; }
    free((void *)heap);
    return 0;
}
