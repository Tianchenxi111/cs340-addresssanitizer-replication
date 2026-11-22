"""Generate a dependency-free SVG from saved Linux/ASan timing summaries."""
from pathlib import Path
import json

root = Path(__file__).resolve().parent
dirs = [root/'results/linux_asan/20261122T120901865770Z',
        root/'results/linux_asan/20261122T121014289041Z']
series = [json.loads((d/'summary.json').read_text()) for d in dirs]
parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="560" viewBox="0 0 1000 560">',
         '<rect width="1000" height="560" fill="white"/>',
         '<style>text{font-family:Arial,sans-serif;fill:#172033}.title{font-size:24px;font-weight:700}.label{font-size:15px}.small{font-size:12px;fill:#475569}</style>',
         '<text x="60" y="45" class="title">Synthetic workload: baseline and AddressSanitizer runtime</text>',
         '<text x="60" y="72" class="small">Ubuntu 24.04.5 / Clang 18.1.3; mean ± sample SD, n=3 per bar; one warmup</text>']
scale = 330/2.8
for tick in (0, 0.5, 1, 1.5, 2, 2.5):
    y = 450-tick*scale
    parts += [f'<line x1="85" y1="{y:.1f}" x2="950" y2="{y:.1f}" stroke="#e2e8f0"/>',
              f'<text x="48" y="{y+5:.1f}" class="small">{tick:.1f}</text>']
parts += ['<text x="20" y="265" transform="rotate(-90 20 265)" class="label">Elapsed seconds</text>']
colors = {'baseline':'#2563eb','asan':'#f97316'}
for j,size in enumerate((8388608,16777216)):
    group_x = (170,570)[j]
    for campaign,data in enumerate(series):
        for mode_index,mode in enumerate(('baseline','asan')):
            row = next(x for x in data if x['size']==size and x['mode']==mode)
            mean,sd = row['mean_seconds'],row['sample_sd_seconds']
            x = group_x+campaign*140+mode_index*62
            y = 450-mean*scale
            parts += [f'<rect x="{x}" y="{y:.1f}" width="52" height="{450-y:.1f}" fill="{colors[mode]}"/>',
                      f'<line x1="{x+26}" y1="{450-(mean+sd)*scale:.1f}" x2="{x+26}" y2="{450-(mean-sd)*scale:.1f}" stroke="#111827" stroke-width="2"/>',
                      f'<text x="{x+26}" y="{y-11:.1f}" text-anchor="middle" class="small">{mean:.2f}</text>']
    parts += [f'<text x="{group_x+122}" y="477" text-anchor="middle" class="label">{size:,} elements</text>',
              f'<text x="{group_x+52}" y="495" text-anchor="middle" class="small">Initial</text>',
              f'<text x="{group_x+192}" y="495" text-anchor="middle" class="small">Rerun</text>']
parts += ['<rect x="350" y="514" width="18" height="18" fill="#2563eb"/>',
          '<text x="375" y="528" class="label">Baseline</text>',
          '<rect x="500" y="514" width="18" height="18" fill="#f97316"/>',
          '<text x="525" y="528" class="label">AddressSanitizer</text>',
          '<text x="500" y="551" text-anchor="middle" class="small">Original workload, not SPEC CPU2006; raw logs in results/linux_asan/</text>', '</svg>']
target=root/'figures'/'asan_runtime.svg'
target.write_text('\n'.join(parts),encoding='utf-8')
print(target)
