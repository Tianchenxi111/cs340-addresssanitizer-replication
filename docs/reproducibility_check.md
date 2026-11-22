# Reproducibility check — 22 November 2026

| Check | Result | Evidence |
|---|---|---|
| Ubuntu/Clang/ASan environment on E: | Pass on this machine | `docs/environment_lock.md`; Ubuntu 24.04.5, Clang 18.1.3 |
| Baseline and instrumented C build | Pass | Build logs in both timing campaigns' `raw_logs.zip` archives |
| Four intended ASan diagnostics | Pass | `detection.json` and stderr files in `raw_logs.zip`; clean control exits 0 |
| Matching checksum for paired benchmark | Pass | Both campaigns' individual stdout and `timings.csv` |
| At least three measured runs per condition | Pass | One warmup plus three measured runs, two sizes and both modes |
| Controlled timing rerun | Pass | `20261122T121014289041Z/`; spread disclosed |
| VmPeak and VmHWM measurement | Pass | `20261122T121426883607Z_memory/` summary and `raw_logs.zip` |
| Clean-machine rebuild from instructions | Pending | No separate clean-machine run performed |
| Paper's original SPEC CPU2006 setup | Not reproduced | Different workload, hardware and ASan settings |

The older local Windows GCC pilot and failed `-lasan` link attempt are excluded from this weekly upload. They do not describe the current Linux setup. All three Linux result directories have `STATUS.txt` marked `COMPLETE`. Their saved files should be reviewed by the group before submission. The original paper's aggregate results cannot receive a supported reproduction verdict from this synthetic workload alone.
