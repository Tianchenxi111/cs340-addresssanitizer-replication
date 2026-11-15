# Experimental protocol and claim boundaries

## Relationship to the previous submission

The previous draft selected the paper's Figure 2 runtime and Table 1 memory
results. This submission implements the first runtime experiment and preliminary
bug-detection checks. Memory measurement remains a separate pending milestone.
The repository's actual remote state could not be retrieved; this package is an
additive submission based on the previous draft in this chat.

## Claim map

| Target | Paper reference | This implementation | Current verdict |
|---|---|---|---|
| Runtime cost of instrumentation | Section 4, Figure 2 | Baseline vs ASan elapsed time on a synthetic workload | Inconclusive: not run |
| Memory overhead | Section 4, Table 1 | Not implemented this week | Inconclusive: not measured |
| Detection of four memory-error classes | Sections 3 and 4.2 | Four original cases plus clean control | Inconclusive: not run |

The last row is a supporting sanity check, not reproduction of the number of bugs
found in Chromium. Detection expectations are heap-buffer-overflow,
stack-buffer-overflow, global-buffer-overflow and heap-use-after-free. A nonzero
exit alone is insufficient: the ASan log must contain the expected diagnostic.
A baseline program's success does not demonstrate absence of a memory bug.

## Setup differences to retain in the final report

| Item | Paper setup | Current protocol | Reason / consequence |
|---|---|---|---|
| Hardware | HP Z600, two Xeon E5620 CPUs, 24 GB RAM | Actual hardware captured when run | Available hardware; absolute timings differ |
| Workload | SPEC CPU2006 | Original synthetic C loop | No confirmed SPEC access; cannot reproduce suite average |
| Compiler | Historical LLVM/Clang, -O2 | Installed Clang, -O2, version recorded and then frozen | Accessible implementation; instrumentation differs |
| Runtime settings | 32-byte redzones, no allocation stack unwinding, zero quarantine | Modern defaults except recorded ASAN_OPTIONS | Pilot detection uses defaults; runtime comparison is not matched |
| Memory metric | VmPeak-based accounting described in Section 4 | None yet | Must implement and inspect metric definition before comparison |

The published average runtime overhead is 73%; the reported memory factor is
3.37x. These are reference values only. Present our pilot alongside them with a
different-workload label; do not calculate a reproduction error against them as
though the experimental settings matched.

## Analysis procedure

For each size, report baseline and instrumented elapsed seconds as mean +/-
sample standard deviation, plus n. Runtime ratio is mean(ASan)/mean(baseline);
overhead is (ratio-1)*100 percent. Every table row must point to its timestamped
logs and run IDs. Use a labeled runtime chart. Report memory in a separate chart
only after a valid measurement method has been implemented.

Extension question: does input size change ASan runtime overhead on this workload?
Change only element count; preserve hardware, compiler, flags, loop rounds and
ASan options. This explores one workload's behavior, not a general performance law.

For unexplained differences, rerun a controlled comparison on the same machine.
Check process startup effects, background load, compiler versions, optimization,
runtime settings and workload differences. Keep original and rerun logs. A cause
remains a hypothesis until evidence supports it. Repeated runs support timing
statistics; they do not establish general detection accuracy.

Source: https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf
