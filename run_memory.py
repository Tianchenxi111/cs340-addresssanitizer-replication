"""Linux VmPeak and VmHWM paired measurements; Python 3.10+."""
import csv
import json
import os
import re
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '_memory')
OUT.mkdir(parents=True)
source = ROOT / 'src' / 'benchmark_memory.c'
build = ROOT / 'build'
build.mkdir(exist_ok=True)
for mode in ('baseline', 'asan'):
    flags = ['-std=c11', '-O2', '-g', '-fno-omit-frame-pointer']
    if mode == 'asan':
        flags.append('-fsanitize=address')
    cmd = ['clang-18', *flags, str(source), '-o', str(build/f'memory-{mode}')]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    (OUT/f'build-{mode}.json').write_text(json.dumps({'command': cmd, 'exit': p.returncode,
                                                      'stdout': p.stdout, 'stderr': p.stderr}, indent=2))
    if p.returncode:
        raise RuntimeError(f'build failed: {mode}')
rows = []
for size in (8388608, 16777216):
    checksums = set()
    for repeat in range(4):
        order = ('baseline', 'asan') if repeat % 2 == 0 else ('asan', 'baseline')
        for mode in order:
            label = f'{size}-{repeat}-{mode}'
            cmd = [str(build/f'memory-{mode}'), str(size)]
            env = os.environ.copy()
            env['ASAN_OPTIONS'] = 'detect_leaks=0:halt_on_error=1:abort_on_error=0:symbolize=1'
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=300, env=env)
            (OUT/f'{label}.stdout.txt').write_text(p.stdout)
            (OUT/f'{label}.stderr.txt').write_text(p.stderr)
            if p.returncode:
                raise RuntimeError(f'run failed: {label}')
            checksums.add(p.stdout.strip())
            values = dict((k, int(v)) for k, v in re.findall(r'^(VmPeak|VmHWM):\s+(\d+) kB$', p.stderr, re.M))
            if set(values) != {'VmPeak', 'VmHWM'}:
                raise RuntimeError(f'memory fields absent: {label}')
            if repeat:
                rows.append({'size': size, 'run': repeat, 'mode': mode,
                             'VmPeak_kB': values['VmPeak'], 'VmHWM_kB': values['VmHWM'],
                             'checksum': p.stdout.strip(), 'log': label})
    if len(checksums) != 1:
        raise RuntimeError(f'checksum mismatch for size {size}')
with (OUT/'memory.csv').open('w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
summary = []
for size in (8388608, 16777216):
    record = {'size': size, 'n_per_mode': 3}
    for metric in ('VmPeak_kB', 'VmHWM_kB'):
        for mode in ('baseline', 'asan'):
            vals = [r[metric] for r in rows if r['size'] == size and r['mode'] == mode]
            record[f'{metric}_{mode}_mean'] = statistics.mean(vals)
            record[f'{metric}_{mode}_sample_sd'] = statistics.stdev(vals)
        record[f'{metric}_asan_to_baseline_ratio'] = (
            record[f'{metric}_asan_mean'] / record[f'{metric}_baseline_mean'])
    summary.append(record)
(OUT/'summary.json').write_text(json.dumps(summary, indent=2))
(OUT/'STATUS.txt').write_text('COMPLETE\n')
print(OUT)
print(json.dumps(summary, indent=2))
