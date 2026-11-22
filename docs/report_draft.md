# AddressSanitizer: A Fast Address Sanity Checker — Replication Report (Draft)

**CS340 Operating Systems — 22 November 2026 experimental draft**

## Research question and source claims

We examine whether AddressSanitizer (ASan) detects representative memory errors and what runtime and memory costs it adds to an original, repeatable C workload. The original paper's Section 4 reports 73% average runtime slowdown on SPEC CPU2006 and a 3.37x aggregate memory factor. We treat those as reference claims, not directly comparable targets: our workload and hardware differ. The final report needs the group's verified author contributions.

## Setup and deviations

The original work used 64-bit Linux, an HP Z600 with Xeon E5620 processors, SPEC CPU2006, Clang `-O2`, and specific ASan options. We used Ubuntu 24.04.5 under WSL 2 on an AMD Ryzen 7 7840H laptop. Ubuntu Clang 18.1.3 compiled the same source with and without `-fsanitize=address` at `-O2 -g -fno-omit-frame-pointer`. The original C benchmark performs 256 rounds of array updates; input counts were 8,388,608 and 16,777,216. `ASAN_OPTIONS=detect_leaks=0:halt_on_error=1:abort_on_error=0:symbolize=1`. We did not set the paper's 32-byte redzone, zero quarantine, or allocation unwind configuration exactly. The benchmark is not SPEC CPU2006.

All run commands, versions, source hashes and metadata are in `results/linux_asan/`; each run's full individual logs are in its `raw_logs.zip`. The setup record is `docs/environment_lock.md`. Timed runs took place on the Linux filesystem inside an E: drive WSL virtual disk. Each configuration had one warmup and three measured runs; measured baseline and ASan order alternated. Timing includes process launch. A second complete timing campaign used the same setup. The memory campaign was separate and also used one warmup plus three trials per mode and size.

## Detection results

ASan reported `heap-buffer-overflow`, `stack-buffer-overflow`, `global-buffer-overflow` and `heap-use-after-free` for the four intentionally faulty test cases. Each instrumented test exited with code 1. The instrumented clean control exited 0 without an ASan error. These are small original cases, not tests drawn from the paper's complete evaluation. Baseline error-case exit codes have undefined behavior and are not evidence of detection. The detection summaries are directly readable in `results/linux_asan/20261122T120901865770Z/` and its controlled rerun; raw diagnostic text and exit-code files are in each directory's `raw_logs.zip`.

## Runtime results

Mean ± sample standard deviation, seconds, three measured runs per mode and size:

| Elements | Campaign | Baseline | ASan | Overhead |
|---:|---|---:|---:|---:|
| 8,388,608 | Initial | 0.8306 ± 0.0145 | 1.2369 ± 0.0202 | 48.9% |
| 16,777,216 | Initial | 1.6424 ± 0.0209 | 2.4576 ± 0.0068 | 49.6% |
| 8,388,608 | Rerun | 0.8499 ± 0.0072 | 1.2957 ± 0.0064 | 52.5% |
| 16,777,216 | Rerun | 1.5491 ± 0.1383 | 2.3833 ± 0.1594 | 53.9% |

All checksum outputs matched at each size. Doubling input size roughly doubled elapsed time in both modes. The input-size extension therefore has measured data for baseline and ASan. Overhead was about 49–54% across these campaigns. The large-input rerun had higher variation than the initial campaign, so both are retained. A possible host scheduling or load effect is an inference, not a proven cause.

`figures/asan_runtime.svg` plots the four paired conditions with sample-SD bars. It is generated from the archived `summary.json` files by `make_asan_chart.py`.

## Memory results

The memory variant read `/proc/self/status` just before exit. `VmHWM` is peak resident memory; `VmPeak` is peak virtual address space. Means ± sample SD (kB), three measured runs:

| Elements | Baseline VmHWM | ASan VmHWM | Resident ratio |
|---:|---:|---:|---:|
| 8,388,608 | 34,505 ± 2 | 38,016 ± 14 | 1.102x |
| 16,777,216 | 67,275 ± 2 | 70,815 ± 51 | 1.053x |

`VmPeak` was 35,464 and 68,232 kB for baseline, versus approximately 21,474,921,576 and 21,474,954,344 kB for ASan. This immense virtual-address figure reflects the runtime's large shadow-memory reservation and is not a physical-memory multiplier. Our `VmHWM` measurement uses a different metric from the paper's reported aggregate memory result. The original Table 1 setting and workloads were not reproduced, so neither of these ratios should be presented as a direct confirmation or refutation of 3.37x.

## Paper comparison, discrepancies and verdict

| Source claim | Paper | This experiment | Verdict |
|---|---:|---:|---|
| SPEC CPU2006 average slowdown | 73% | 49–54% on one synthetic program | Inconclusive for paper claim |
| Aggregate memory factor | 3.37x | 1.05–1.10x VmHWM on one synthetic program; VmPeak affected by virtual reservation | Inconclusive for paper claim |
| Detection of representative bugs | Address and lifetime errors | Four expected ASan diagnostics observed | Supported for our small cases |

The performance gap from the paper is expected to depend on workload, CPU, compiler/runtime generation, ASan settings and timing method. We cannot assign a measured share to each cause. The controlled rerun showed a 3.6–4.2 percentage-point increase in overhead across the two sizes, with high timing spread at the larger size. We retain all runs rather than choosing the more favorable campaign. Matching SPEC CPU2006 and the original configuration would be needed to evaluate the paper's aggregate numbers directly.

## Reproducibility and remaining work

The combined repository's sources and scripts generated complete results on this machine. The earlier local Windows GCC baseline and ASan link failure are excluded from this weekly upload and are not mixed with Linux/ASan measurements. A separate clean-machine rebuild and run, final English PDF, final presentation under the course's separate presentation instructions, and reviewed member-by-member contribution details remain pending. The group should inspect the logs and repeat the commands before final submission.

## Contributions and AI usage

**Tian Chenxi (1240021771):** selected the AddressSanitizer paper, created and managed the group GitHub repository, invited collaborators, and organized the weekly submission files and milestones.

**AI assistance:** An AI assistant helped draft experiment scripts, protocol notes, and report text, and assisted with configuring the local Linux/Clang environment and running the recorded tests. The reported measurements come from saved program outputs on the project computer.

## References

1. K. Serebryany et al., “AddressSanitizer: A Fast Address Sanity Checker,” USENIX ATC 2012. https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
2. Clang documentation, “AddressSanitizer.” https://clang.llvm.org/docs/AddressSanitizer.html
