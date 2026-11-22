# CS340 AddressSanitizer replication — 22 November update

This folder is an additive update to the existing group repository. Keep the earlier repository README and work. `src/benchmark.c` replaces last week's version only to make its checksum format portable; its calculation is unchanged.

Upload these files into the existing repository while preserving their folder paths. Last week's `run.py` and `src/detection.c` have not changed, so they are deliberately omitted from this weekly upload. The new memory runner and the report rely on those files already being in the repository. Keep the root `README.md` and `.gitignore` from last week.

## Verified results

Ubuntu 24.04.5 and Clang 18.1.3 with the ASan runtime were installed and tested in a WSL 2 virtual disk on E:. Heap, stack and global overflow and heap use-after-free each produced the expected ASan diagnostic. The clean instrumented control exited 0. Baseline and ASan workloads completed two three-run timing campaigns at two input sizes. Initial overhead was 48.9% and 49.6%; controlled-rerun overhead was 52.5% and 53.9%. The input-size extension and a separate three-run resident-memory measurement also completed. Summaries, commands and environment metadata are readable in `results/linux_asan/`; each run's `raw_logs.zip` contains all original files. See `results/linux_asan/README.md` for archive details and `docs/experiment_status.md` for values and limitations.

The earlier local Windows GCC pilot and failed ASan link attempt are excluded from this upload; only the successful Linux/ASan results are included. A final English report draft and presentation outline are in `docs/`. The paper's SPEC average slowdown and aggregate memory factor remain inconclusive on our different workload and hardware.

`figures/asan_runtime.svg` is the Linux paired-runtime chart.

## Reproduce in Ubuntu

Install Ubuntu 24.04 and packages `python3 clang-18 libclang-rt-18-dev`. Copy the combined repository's `run.py`, `run_memory.py` and `src/` folder into a directory on the Ubuntu filesystem. From that directory run:

```bash
python3 run.py --cc clang-18 --runs 3 --sizes 8388608 16777216
python3 run_memory.py
```

Each script creates a timestamped `results/` folder. The main runner saves detection logs, baseline/ASan measurements and environment data. The memory runner saves raw `VmPeak` and `VmHWM` values. Full environment settings, deviations and original source hashes are recorded in `docs/environment_lock.md`. No external benchmark data or Python libraries are required. A separate clean-machine reproduction is still pending.

## Before December 1

The group should review the scripts and logs, attempt the documented run on a separate clean setup, finish the final English PDF and slides, and verify the individual contribution and AI-usage statements required in the final report. Check the course's separate Presentation Instruction. Submit the required repository link and tag the reviewed final repository `v1.0` only when final materials are complete.

Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
