/* Original, defined-behavior synthetic workload; not SPEC CPU2006. */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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
    /* Hex avoids the old MinGW/MSVCRT unsigned-long-long printf mismatch. */
    printf("%08x%08x\n", (unsigned)(sum >> 32), (unsigned)sum);
    /* Match the paper's Linux VmPeak field; VmHWM is also retained. */
    FILE *status = fopen("/proc/self/status", "r");
    if (!status) return 4;
    char line[256];
    while (fgets(line, sizeof(line), status)) {
        if (strncmp(line, "VmPeak:", 7) == 0 || strncmp(line, "VmHWM:", 6) == 0)
            fputs(line, stderr);
    }
    fclose(status);
    free((void *)data);
    return 0;
}
