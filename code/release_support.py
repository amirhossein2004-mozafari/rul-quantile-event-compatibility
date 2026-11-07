"""Read original relative input names through the public release index."""
import csv
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / 'docs/file_index.csv').open(encoding='utf-8', newline='') as stream:
    INDEX = {row['source_relative']: row for row in csv.DictReader(stream)}


class IndexedPath:
    """Small path adapter for the two unchanged historical arithmetic scripts."""

    def __init__(self, value='.'):
        text = str(value).replace('\\', '/')
        native = Path(text)
        if native.is_absolute():
            text = native.resolve().relative_to(ROOT).as_posix()
        self.virtual = PurePosixPath(text)
        if '..' in self.virtual.parts:
            raise ValueError('Paths must stay within the release')

    def __truediv__(self, other):
        return IndexedPath(self.virtual / str(other))

    def __str__(self):
        return str(self.virtual)

    def __lt__(self, other):
        return self.virtual.as_posix() < other.virtual.as_posix()

    def __fspath__(self):
        return str(self.native)

    @property
    def native(self):
        key = self.virtual.as_posix()
        return ROOT / INDEX.get(key, {}).get('release_relative', key)

    @property
    def name(self):
        return self.virtual.name

    @property
    def parent(self):
        return IndexedPath(self.virtual.parent)

    @property
    def parents(self):
        return [IndexedPath(parent) for parent in self.virtual.parents]

    def resolve(self):
        return self

    def exists(self):
        return self.native.exists()

    def with_name(self, name):
        return IndexedPath(self.virtual.with_name(name))

    def glob(self, pattern):
        prefix = self.virtual.as_posix().rstrip('/') + '/'
        depth = len(PurePosixPath(pattern).parts)
        for key in sorted(INDEX):
            if key.startswith(prefix):
                tail = PurePosixPath(key[len(prefix):])
                if len(tail.parts) == depth and tail.match(pattern):
                    yield IndexedPath(key)

    def open(self, *args, **kwargs):
        return self.native.open(*args, **kwargs)

    def read_text(self, *args, **kwargs):
        if self.virtual.as_posix() == 'FILE_MANIFEST.json':
            return json.dumps({'files': {name: row['release_sha256'] for name, row in INDEX.items()}})
        return self.native.read_text(*args, **kwargs)

    def read_bytes(self):
        return self.native.read_bytes()

    def mkdir(self, *args, **kwargs):
        return self.native.mkdir(*args, **kwargs)

    def write_text(self, *args, **kwargs):
        return self.native.write_text(*args, **kwargs)
