/* Original, defined-behavior synthetic workload; not SPEC CPU2006. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc != 2) return 2;
    unsigned long n = strtoul(argv[1], NULL, 10);
    if (n < 1024 || n > 16777216) return 2;
    volatile uint32_t *data = malloc(n * sizeof(*data));
    if (!data) return 3;
    for (unsigned long i = 0; i < n; ++i) data[i] = (uint32_t)i;
    uint64_t sum = 0;
    for (unsigned round = 0; round < 256; ++round)
        for (unsigned long i = 0; i < n; ++i) {
            data[i] = data[i] * 1664525u + 1013904223u;
            sum += data[i];
        }
    printf("%llu\n", (unsigned long long)sum);
    free((void *)data);
    return 0;
}
