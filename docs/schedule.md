# Remaining schedule: November 15 to December 1, 2026

## November 15 (Sunday): this week's deliverable

Submit the source files, runner, protocol and this schedule. Review all files and
push a substantive commit before 23:59. Experiments remain pending until run.
Do not backdate commits or invent progress for earlier weeks.

## November 16-22: environment and measurements

- November 16-17: freeze a Linux environment; save setup instructions and version
  lock; compile and inspect all detection cases and the clean control.
- November 18-20: collect baseline and ASan runtime logs, at least three runs per
  setting. Run the input-size extension. Implement memory measurement with a
  precisely documented metric. Decide whether SPEC or another suitable upstream
  workload is feasible. Keep any new workload distinct from the synthetic pilot.
- November 21-22: produce initial charts, mean +/- SD tables and a complete
  deviations table. Inspect failed expectations and rerun controlled checks.
- By Sunday November 22, 23:59: push scripts, environment specification, raw logs,
  summaries and an English progress note. If blocked, submit real code/document
  progress and describe the blocker; do not invent measurements.

## November 23-29: evidence, report and presentation

- November 23-25: analyze gaps, perform controlled reruns, assign a verdict to
  each claim, and write limitations. Finalize the extension results.
- November 26-27: finish the English report draft: introduction, setup, results,
  discrepancy analysis, extension, conclusion and references. Number and cite
  figures/tables; add an accurate contribution statement.
- November 28-29: reproduce on a clean VM/machine using only the README; fix
  missing steps. Prepare slides according to the separate Presentation Instruction,
  which has not been supplied here. Rehearse and check each reported number.
- By Sunday November 29, 23:59: push final experimental evidence, report draft,
  presentation draft and reproducibility fixes.

## November 30: freeze and rehearse

Resolve remaining discrepancies, export the English report as PDF, rehearse with
all four members, and verify README commands and source attribution. Tag the
reviewed final commit `v1.0` after required files and logs are included. Check the
course notices for report upload location and exact deadline, which were not
specified in the assignment text available here. Do not assume the presentation
date automatically defines every other deadline.

## December 1: presentation

Deliver the group presentation and submit required materials through the actual
course channels. Keep the tagged repository consistent with the presented data.

## Contribution arrangement

Suggested roles to agree as a group: (1) environment and detection, (2) runtime
and extension, (3) memory measurement and statistics, (4) report and slides.
All members review the interpretation and rehearse. Roles are suggestions, not a
claim that any named member has already performed them. Each member commits
substantive work from their own account. Every commit message includes that
member's student ID, full name and a description of the change.

Weekly checks require at least one substantive group commit pushed by Sunday
23:59. Late pushes count toward the next week. Keep build products, disk images,
large traces, files over 50 MB and credentials out of Git. Include a .gitignore;
retain small raw result logs needed to trace the report's numbers.
