"""Verify public payload checksums and unchanged immutable source copies."""
import argparse
import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def public_files():
    for path in ROOT.rglob('*'):
        relative = path.relative_to(ROOT)
        if set(relative.parts) & {'.git', '.build', '__pycache__'}:
            continue
        if relative.parts[:2] == ('docs', 'phase1_inventory'):
            continue
        if path.is_file() and relative.as_posix() != 'CHECKSUMS.sha256':
            yield relative.as_posix(), path


def checksums():
    expected = {}
    for line in (ROOT/'CHECKSUMS.sha256').read_text(encoding='utf-8').splitlines():
        value, name = line.split('  ', 1)
        assert not Path(name).is_absolute() and '..' not in Path(name).parts
        expected[name] = value
    actual = dict(public_files())
    assert set(actual) == set(expected), 'Payload file list differs from the checksum manifest'
    for name, path in actual.items():
        assert digest(path) == expected[name], name
    print(f'PASS: {len(actual)} public payload files match CHECKSUMS.sha256')


def locks():
    with (ROOT/'docs/file_index.csv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    immutable = [row for row in rows if row['verbatim'] == 'True']
    for row in immutable:
        assert digest(ROOT/row['release_relative']) == row['source_sha256'], row['source_relative']
    with (ROOT/'docs/excluded_hash_referenced.csv').open(encoding='utf-8', newline='') as stream:
        excluded = list(csv.DictReader(stream))
    assert len(excluded) == 185 and all(len(row['sha256']) == 64 for row in excluded)
    print(f'PASS: {len(immutable)} immutable source copies unchanged; 185 omitted file digests documented')
    print('Verification of omitted inputs requires the full local archive.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['checksums', 'locks'])
    action = parser.parse_args().action
    {'checksums': checksums, 'locks': locks}[action]()
