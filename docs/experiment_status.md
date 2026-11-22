# Experiment status — 22 November 2026

## Completed and verified

Ubuntu 24.04.5 LTS in WSL 2 and Clang 18.1.3 with its ASan runtime were installed in a virtual disk on E:. Linux baseline and instrumented programs both compiled and ran. Heap, stack and global buffer overflow and heap use-after-free each produced the expected ASan diagnostic and nonzero exit; the clean instrumented control exited 0. The uninstrumented bug cases have undefined behavior, so their exit codes are not interpreted as detection results.

Two full timing campaigns used the same source and parameters. Each size and mode had one warmup and three measured runs; measured order alternated. All checksum outputs agreed within each size. Means and sample standard deviations are in seconds:

| Elements | Campaign | Baseline (n=3) | ASan (n=3) | ASan overhead |
|---:|---|---:|---:|---:|
| 8,388,608 | Initial | 0.8306 ± 0.0145 | 1.2369 ± 0.0202 | 48.9% |
| 16,777,216 | Initial | 1.6424 ± 0.0209 | 2.4576 ± 0.0068 | 49.6% |
| 8,388,608 | Controlled rerun | 0.8499 ± 0.0072 | 1.2957 ± 0.0064 | 52.5% |
| 16,777,216 | Controlled rerun | 1.5491 ± 0.1383 | 2.3833 ± 0.1594 | 53.9% |

The controlled rerun has noticeable spread at the larger size; report both campaigns. Runtime overhead remained roughly 49–54% across the two sizes and campaigns for **this synthetic workload**. The input-size extension is complete for both modes.

The separate memory campaign used one warmup plus three measured runs per size and mode, reading Linux `/proc/self/status` before process exit:

| Elements | Baseline VmHWM, kB | ASan VmHWM, kB | Ratio |
|---:|---:|---:|---:|
| 8,388,608 | 34,505 ± 2 | 38,016 ± 14 | 1.102x |
| 16,777,216 | 67,275 ± 2 | 70,815 ± 51 | 1.053x |

`VmHWM` measures peak resident memory. `VmPeak` measures peak virtual address space. Under this Clang/ASan runtime, it was about 21,474,921,576 kB and 21,474,954,344 kB at the two sizes, versus baseline 35,464 and 68,232 kB. ASan reserves a very large virtual shadow region; these `VmPeak` ratios are not physical memory overhead. Values are in `results/linux_asan/20261122T121426883607Z_memory/memory.csv`; individual logs are in that directory's `raw_logs.zip`.

## Paper comparison and limitations

The paper reports 73% average slowdown on SPEC CPU2006 and a 3.37x aggregate memory factor. Its hardware, workloads and ASan configuration differ from ours. Our 49–54% runtime overhead and VmHWM ratios cannot be used as a direct numeric reproduction of those aggregate results. The four detection mechanisms are supported by the small test cases; the paper's SPEC performance and aggregate memory claims remain **inconclusive** in our setting. A separate clean-machine reproduction and the final report/presentation review remain pending.

Timing records: `results/linux_asan/20261122T120901865770Z/` and `results/linux_asan/20261122T121014289041Z/`. Commands, source hashes, environment, individual times and completion markers are directly readable; raw stdout/stderr and the full original file sets are in each directory's `raw_logs.zip`.

Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
