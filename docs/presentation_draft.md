# Presentation content draft — AddressSanitizer replication

The course's separate Presentation Instruction was not supplied. Confirm its slide/time rules before finalizing.

1. **Question and team:** Can we observe ASan memory-error detection and measure its costs? Introduce all four presenters and their verified roles.
2. **Paper:** Section 4 reports 73% average SPEC CPU2006 slowdown and 3.37x aggregate memory usage. State original Linux/Clang/SPEC setting.
3. **Our design:** Ubuntu 24.04.5 in WSL 2, Clang 18.1.3, original C workload, baseline versus `-fsanitize=address`, three measured runs after warmup, two input sizes and two timing campaigns. Disclose deviations.
4. **Detection:** Show one short raw ASan diagnostic each for heap, stack, global and use-after-free; explain clean-control exit 0. Source: `detection.json` and the timestamped `results/linux_asan/<run>/raw_logs.zip` archives.
5. **Runtime:** Initial overhead 48.9% and 49.6%; rerun 52.5% and 53.9% at 8.39M and 16.78M elements. Display mean ± sample SD and note large-input rerun spread.
6. **Memory and interpretation:** Peak resident memory (`VmHWM`) ratios 1.102x and 1.053x. ASan virtual-address reservation makes `VmPeak` enormous; distinguish it from resident memory. Neither metric directly replicates the paper's aggregate table.
7. **Conclusion and limits:** Detection works for four small cases. Paper's SPEC runtime and aggregate memory claims remain inconclusive because hardware, workload and ASan settings differ. Explain input-size extension, remaining clean-machine run, and evidence path.

Each speaker should describe only work they personally completed. Before December 1, replace this outline with a reviewed slide deck and check every value against the archived logs.
