"""Run original arithmetic with public input mapping and saved-label checks.

The original scripts remain byte-identical. Two adaptations are applied in
memory: source-relative paths use file_index.csv, and official raw-data label
checks become saved-label consistency checks. No inference or bootstrap runs.
"""
import argparse
import json
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('check', choices=['csv', 'cross-head'])
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    if args.check == 'csv':
        script = ROOT / 'code/review/remaining_step10_packet/reproduce_csv.py'
        old = "truth=[float(x) for x in (root/f'data/raw/cmapss/RUL_{subset}.txt').read_text().split()]"
        new = "truth=[float(row[yk]) for row in sorted(test,key=lambda row:int(row['engine_id']))]"
    else:
        script = ROOT / 'code/scripts/reproduce_cross_head.py'
        old = "truth=[float(s) for s in (root/f'data/raw/cmapss/RUL_{sub}.txt').read_text().split()]"
        new = "truth=[float(row['raw_y']) for row in sorted(rows,key=lambda row:int(row['engine_id']))]"
    source = script.read_text(encoding='utf-8-sig')
    assert source.count(old) == 1, 'Historical label-check implementation changed'
    assert source.count('from pathlib import Path') == 1
    source = source.replace('from pathlib import Path', 'from release_support import IndexedPath as Path')
    source = source.replace(old, new)
    if args.check == 'cross-head':
        # The optional example CSV was outside the approved copy list.
        block = "    for r in read(base/'extremal_examples.csv'):\n        best=sorted([x for x in per if x['method']==r['method']],key=lambda x:(-float(x['distance']),x['subset'],x['model'],int(x['seed']),int(x['engine_id'])))[0]\n        assert best==r\n"
        assert source.count(block) == 1
        source = source.replace(block, '')
    output = args.output_dir or f'.build/checks/{args.check}_{uuid.uuid4().hex[:10]}'
    target = (ROOT / output).resolve()
    assert target.is_relative_to(ROOT) and not target.exists()
    target.parent.mkdir(parents=True, exist_ok=True)
    sys.argv = [str(script), '--root', '.', '--output-dir', output]
    exec(compile(source, script.name, 'exec'), {'__name__': '__main__', '__file__': str(script)})
    record_path = target / 'summary.json'
    record = json.loads(record_path.read_text(encoding='utf-8'))
    record['public_release_adaptations'] = [
        'Original input names resolved through docs/file_index.csv',
        'Input manifest checks verify the indexed release bytes',
        'Saved-label consistency replaces comparison with excluded official NASA labels',
    ]
    record['independent_official_label_verification'] = False
    if args.check == 'cross-head':
        record['optional_extremal_example_verification'] = 'Not run: example CSV was not in the approved copy list'
    record_path.write_text(json.dumps(record, indent=2), encoding='utf-8')
    print('Public check record: ' + record_path.relative_to(ROOT).as_posix())


if __name__ == '__main__':
    main()
