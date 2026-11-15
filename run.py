"""Linux experiment runner. Logs every command and output; Python 3.10+."""
import argparse
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cc', default='clang')
    parser.add_argument('--runs', type=int, default=3)
    parser.add_argument('--sizes', type=int, nargs='+', default=[262144, 1048576])
    args = parser.parse_args()
    if args.runs < 3 or len(set(args.sizes)) != len(args.sizes) or any(
        n < 1024 or n > 16777216 for n in args.sizes
    ):
        parser.error('Use >=3 runs, unique sizes in [1024,16777216].')
    if platform.system() != 'Linux' or not shutil.which(args.cc):
        parser.error('Requires Linux and Clang on PATH; no measurements performed.')
    out = ROOT / 'results' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    out.mkdir(parents=True)
    build = ROOT / 'build'
    build.mkdir(exist_ok=True)
    env = os.environ.copy()
    env['ASAN_OPTIONS'] = 'detect_leaks=0:halt_on_error=1:abort_on_error=0:symbolize=1'
    for key in ('LSAN_OPTIONS', 'UBSAN_OPTIONS', 'ASAN_SYMBOLIZER_PATH'):
        env.pop(key, None)
    commands = []
    def call(cmd, label, required=True):
        commands.append({'label': label, 'argv': [str(x) for x in cmd]})
        (out / 'commands.json').write_text(json.dumps(commands, indent=2))
        try:
            started = time.perf_counter()
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
            result.elapsed_seconds = time.perf_counter() - started
        except subprocess.TimeoutExpired as exc:
            (out / (label + '.timeout.txt')).write_text(str(exc))
            raise RuntimeError('Timeout; incomplete run, see logs') from exc
        (out / (label + '.stdout.txt')).write_text(result.stdout)
        (out / (label + '.stderr.txt')).write_text(result.stderr)
        (out / (label + '.exit.txt')).write_text(str(result.returncode))
        if required and result.returncode:
            raise RuntimeError(f'{label} failed; see logs')
        return result
    version = call([args.cc, '--version'], 'compiler').stdout
    if 'clang' not in version.lower():
        raise RuntimeError('This protocol requires Clang.')
    metadata = {'utc': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
                'kernel': platform.release(), 'machine': platform.machine(),
                'python': sys.version, 'compiler': version, 'runs': args.runs,
                'sizes': args.sizes, 'ASAN_OPTIONS': env['ASAN_OPTIONS'],
                'sources_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in [ROOT/'run.py', *sorted((ROOT/'src').glob('*.c'))]}}
    for name in ('/etc/os-release', '/proc/cpuinfo', '/proc/meminfo'):
        if Path(name).exists():
            (out / (Path(name).name + '.txt')).write_text(Path(name).read_text())
    if shutil.which('git'):
        head = call(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], 'starting_commit', False)
        metadata['starting_commit'] = head.stdout.strip() if head.returncode == 0 else 'not in a Git checkout'
        call(['git', '-C', str(ROOT), 'status', '--short'], 'git_status', False)
    (out / 'environment.json').write_text(json.dumps(metadata, indent=2))
    for mode in ('baseline', 'asan'):
        flags = ['-std=c11', '-O2', '-g', '-fno-omit-frame-pointer']
        if mode == 'asan': flags += ['-fsanitize=address']
        for source in ('detection', 'benchmark'):
            call([args.cc, *flags, str(ROOT/'src'/f'{source}.c'), '-o', str(build/f'{source}-{mode}')],
                 f'build-{source}-{mode}')
    expected = {'heap': 'heap-buffer-overflow', 'stack': 'stack-buffer-overflow',
                'global': 'global-buffer-overflow', 'uaf': 'heap-use-after-free'}
    detections = []
    for case in (*expected, 'clean'):
        for mode in ('baseline', 'asan'):
            r = call([str(build/f'detection-{mode}'), case], f'detection-{case}-{mode}', False)
            match = (r.returncode != 0 and expected[case] in r.stderr) if case != 'clean' else (
                r.returncode == 0 and 'ERROR: AddressSanitizer' not in r.stderr)
            detections.append({'case': case, 'mode': mode, 'exit': r.returncode,
                               'expected_asan_behavior': match if mode == 'asan' else None})
    (out/'detection.json').write_text(json.dumps(detections, indent=2))
    rows, summaries = [], []
    for size in args.sizes:
        outputs, times = set(), {'baseline': [], 'asan': []}
        for mode in times:
            call([str(build/f'benchmark-{mode}'), str(size)], f'warmup-{size}-{mode}')
        for repeat in range(args.runs):
            order = ('baseline', 'asan') if repeat % 2 == 0 else ('asan', 'baseline')
            for mode in order:
                label = f'bench-{size}-{repeat+1}-{mode}'
                r = call([str(build/f'benchmark-{mode}'), str(size)], label)
                elapsed = r.elapsed_seconds
                times[mode].append(elapsed)
                outputs.add(r.stdout.strip())
                rows.append({'size': size, 'run': repeat+1, 'mode': mode,
                             'seconds': elapsed, 'log_prefix': label})
        if len(outputs) != 1:
            raise RuntimeError('Checksums differ; reject timing comparison')
        for mode, values in times.items():
            summaries.append({'size': size, 'mode': mode, 'mean_seconds': statistics.mean(values),
                              'sample_sd_seconds': statistics.stdev(values), 'runs': len(values)})
        ratio = statistics.mean(times['asan']) / statistics.mean(times['baseline'])
        summaries.append({'size': size, 'asan_to_baseline_ratio': ratio, 'overhead_percent': (ratio-1)*100})
    with (out/'timings.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys()); writer.writeheader(); writer.writerows(rows)
    (out/'summary.json').write_text(json.dumps(summaries, indent=2))
    failed = any(not x['expected_asan_behavior'] for x in detections if x['mode'] == 'asan')
    status = 'REVIEW_REQUIRED' if failed else 'COMPLETE'
    (out/'STATUS.txt').write_text(status + '\n')
    print(f'{status}: {out}')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
