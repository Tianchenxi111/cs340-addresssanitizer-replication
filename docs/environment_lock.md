# Environment record — 22 November 2026

| Component | Verified value |
|---|---|
| Host | Lenovo laptop, AMD Ryzen 7 7840H, Windows 11 build 26200 |
| Guest | Ubuntu 24.04.5 LTS, WSL 2, x86_64 |
| Guest kernel | 6.18.58.1-microsoft-standard-WSL2 |
| Guest storage | `E:\WSL\Ubuntu-24.04\ext4.vhdx` |
| Compiler | Ubuntu Clang 18.1.3 (`clang-18`), `libclang-rt-18-dev` installed |
| Python | Ubuntu system Python 3; exact version in each `environment.json` |
| Build flags | `-std=c11 -O2 -g -fno-omit-frame-pointer`, plus `-fsanitize=address` for ASan |
| ASAN_OPTIONS | `detect_leaks=0:halt_on_error=1:abort_on_error=0:symbolize=1` |
| Workload | Original `src/benchmark.c`, 256 rounds; 8,388,608 and 16,777,216 elements |
| Timer | Python `time.perf_counter()` including process launch |
| Trials | One warmup plus three measured runs per size and mode; alternating measured order |
| Benchmark SHA-256 | `8783bd5fc95090b708125515b32dfc886cdfed2a946ea80835a1f41f6a30a4f9` |
| Detection SHA-256 | `5bd20facd89366662fd6116521323da2ddd45bf8a50e66edfe2c2240b5b7faf0` |

In Ubuntu, copy the combined repository's `run.py`, `run_memory.py` and `src/` to a Linux filesystem directory before measuring. The existing `run.py` and `src/detection.c` were submitted last week and are not repeated in this weekly upload. The experiment was run from `/root/asan-replication-20261122` within the E: VHD. In that directory:

```bash
python3 run.py --cc clang-18 --runs 3 --sizes 8388608 16777216
python3 run_memory.py
```

The first command compiles both modes and saves detection diagnostics, raw timing logs, and environment metadata in a timestamped `results/` directory. The second uses `src/benchmark_memory.c` and reads `VmPeak` and `VmHWM` from `/proc/self/status`. It likewise saves individual logs and a summary. Copying to the Linux filesystem avoids WSL `/mnt/c` filesystem overhead in the timed runs. The full original files from two timing campaigns and one memory campaign are preserved in each `results/linux_asan/<run>/raw_logs.zip`; summaries and key metadata remain directly readable beside each archive.

The earlier local Windows/MinGW baseline pilot and failed `-lasan` link attempt are not included in this weekly upload. The Linux environment was successfully tested on this machine, but a separate clean-machine rebuild has not yet been performed. The paper used a different processor and the SPEC CPU2006 suite; these experiments use an original synthetic program.
