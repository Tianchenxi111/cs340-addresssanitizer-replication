田晨曦 1240021771
刘语哲 1240025695
龙振湘 1240036717
徐一笑 1240035180
Paper
Konstantin Serebryany, Derek Bruening, Alexander Potapenko, and Dmitry Vyukov. “AddressSanitizer: A Fast Address Sanity Checker.” USENIX ATC, 2012.
Paper: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf

Project Goal
We will reproduce selected findings from the AddressSanitizer paper. Our initial plan is to test whether AddressSanitizer detects a memory error in a small test program and to measure its runtime overhead compared with the same program compiled without AddressSanitizer.
After reviewing the paper’s figures and tables, we will identify the specific claims and results that our experiments can reasonably compare with. Any differences between the paper’s setup and ours will be recorded.

Planned Experiments
Error detection: Run a test program containing a known memory error with and without AddressSanitizer. Record whether the error is detected and save the diagnostic output.
Runtime overhead: Run the same workload with and without AddressSanitizer under the same conditions. Repeat each measurement at least three times and report the mean and standard deviation.
Extension: Change one workload factor, such as input size, while keeping the other experimental conditions fixed. Examine how this affects the measured overhead.

Reproducibility Plan
We will add the test programs, build and run commands, workload inputs, and result logs to this repository. We will record the operating system, kernel, compiler, AddressSanitizer version, hardware, and relevant settings. The README will be updated with steps for reproducing the final results.

Current Status
The repository and project plan have been created. The paper claims, experimental setup, scripts, and results are still being developed.

## Week 1: Replication Scope and Experimental Plan

### Paper Results Selected for Investigation

We will investigate two results from Section 4 of the AddressSanitizer paper:

1. **Runtime overhead (Figure 2):** The paper reports an average slowdown of 73% for AddressSanitizer on SPEC CPU2006 benchmarks.
2. **Memory usage (Table 1):** The paper reports an overall memory usage increase of 3.37× for the evaluated benchmarks.

These are the paper's results, not results obtained by our group.

### Original Experimental Setup

The paper used 64-bit Linux on an HP Z600 workstation with two quad-core Intel Xeon E5620 processors and 24 GB of RAM. It compared AddressSanitizer-instrumented binaries with binaries compiled using regular Clang at `-O2`. The experiments used SPEC CPU2006 benchmarks, 32-byte redzones, disabled stack unwinding during allocation and deallocation, and a quarantine size of zero.

### Planned Reduced-Scale Reproduction

We will first identify a benchmark that we can obtain and run legally in our environment. We will compile the same source code in two configurations: a baseline build and an AddressSanitizer build. We will run each configuration at least three times with the same input and machine settings, retain the raw logs, and calculate the mean and standard deviation of runtime. Where supported by our operating system, we will also measure peak memory usage.

We will compare results using the same units and ratios as the paper. We will not present a small benchmark as a direct reproduction of the paper's SPEC CPU2006 average.

### Deviations to Record Before Running

| Item | Paper setup | Our setup |
|---|---|---|
| Hardware | HP Z600; two Intel Xeon E5620 CPUs; 24 GB RAM | To be recorded |
| Operating system | 64-bit Linux | To be recorded |
| Compiler | Clang with `-O2` | To be recorded |
| Workloads | SPEC CPU2006 | To be selected |
| AddressSanitizer settings | 32-byte redzones; allocation stack unwinding disabled; quarantine size zero | To be recorded |
| Number of runs | Not stated for each measurement in Section 4 | At least three per configuration |

### Next Steps

1. Record our hardware, operating system, kernel, and compiler versions.
2. Select and document the benchmark and its input.
3. Add build and run scripts so another person can repeat the experiment.
4. Save unmodified run logs and produce a “Paper vs. Ours” table.
5. Explain every important setup difference and its possible effect on the comparison.
