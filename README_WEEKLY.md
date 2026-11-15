# November 15 submission: experiment harness and protocol

This supplements the existing repository README. Merge its run instructions into
that README; keep the existing team information. All paths below assume these
files are placed in the repository root, with `src/` and `docs/` preserved.

## Delivered this week

- Four original C memory-error cases and one valid-memory control.
- A defined-behavior synthetic workload with a printed checksum.
- A Python runner that builds baseline and ASan versions, records commands,
  compiler/OS/kernel/hardware metadata, source hashes and Git state, and retains
  stdout, stderr and exit status for every invocation.
- At least three timing measurements per configuration, sample standard
  deviations, checksum checks and alternating execution order.
- An input-size extension and a dated plan through the December 1 presentation.

## Run on Linux

Prerequisites: Linux, Python 3.10 or newer, Clang with a working compiler-rt ASan
runtime, and optionally Git and llvm-symbolizer. Check `clang --version` and
`python3 --version` first. There are no Python package dependencies or downloads
of workloads: all inputs are generated deterministically by our C program.

```sh
python3 run.py --cc clang --runs 3
```

Expected duration: allow several minutes on a typical laptop; this estimate has
not been calibrated locally. Each subprocess has a five-minute timeout. The
runner stops on build failures, timeouts or checksum mismatches. Memory-error
programs intentionally fail; their exits are captured rather than stopping the
entire run. Valid baseline programs must complete successfully.

Outputs: `results/<UTC timestamp>/` contains raw logs, `environment.json`,
`commands.json`, `detection.json`, `timings.csv`, `summary.json` and `STATUS.txt`.
Only a completed run has STATUS. `REVIEW_REQUIRED` means a detection expectation
was unmet. It is an observation to investigate, not permission to edit the logs.
Compiled executables go in ignored `build/`.

The default sizes are 262144 and 1048576 elements; all other workload parameters
stay fixed. Runtime includes process startup and ASan initialization. The runner
does not measure memory overhead. Do not compare RSS with the paper's VmPeak.
If a timing is under one second, increase both sizes within the documented limit
and repeat the entire experiment; record that deviation. Save all earlier logs.

## Environment freeze gate (before November 22 measurements)

The environment is not yet pinned. Select one Linux machine or VM, install one
specific compiler build, record full package versions and setup commands in
`docs/environment-lock.md`, and preserve a VM snapshot or container image digest.
Include runtime and Python versions. Repeat runs on that frozen environment.
The automatically captured metadata supplements this lock, but does not replace
an installable environment specification. Record starting Git commit, original
code licenses, and modified files for any upstream benchmark added later.

## Honest current status

The submission contains implemented experiment code and a protocol. No ASan
measurement has been obtained: the preparation environment has no usable
Clang/Linux setup. Syntax and failure-path checks are documented separately
in `docs/validation.md`. No numerical reproduction verdict is claimed.

## Sources and attribution

- Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
- Compiler usage: https://clang.llvm.org/docs/AddressSanitizer.html

The C cases and runner are newly written for this project; no upstream source
files have been imported. If upstream code is later used, preserve its license,
credit its authors, record its starting commit and list modified files.

Team members should review and understand the code and protocol before running
the experiments. The final report should record each member's actual contribution.
