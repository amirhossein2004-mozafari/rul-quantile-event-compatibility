"""Compile the readable manuscript and S0-S14 supplement, without analysis."""
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / '.build/pdf'


def compile_pdf(folder, source, header, output, supplement=False):
    build = BUILD / ('supplement' if supplement else 'manuscript')
    build.mkdir(parents=True, exist_ok=True)
    tex = build / 'document.tex'
    command = ['pandoc', source, '--standalone', '--resource-path=.',
               '--include-in-header=' + header, '-V', 'papersize=a4',
               '-V', 'mainfont=Times New Roman', '-V', 'sansfont=Arial',
               '-V', 'monofont=Consolas', '-V', 'fontsize=' + ('10pt' if supplement else '11pt'),
               '-V', 'geometry:margin=' + ('0.75in' if supplement else '0.85in'), '-o', str(tex)]
    if supplement:
        landscape = build / 'landscape.tex'
        landscape.write_text('\\usepackage{pdflscape}\n', encoding='utf-8')
        command.append('--include-in-header=' + str(landscape))
    else:
        command.extend(['--citeproc', '--bibliography=references.bib'])
    subprocess.run(command, cwd=ROOT/folder, check=True, capture_output=True)
    text = tex.read_text(encoding='utf-8')
    text = re.sub(r'(?<![a-f0-9])([a-f0-9]{64})(?![a-f0-9])', r'\\seqsplit{\1}', text)
    tex.write_text(text, encoding='utf-8')
    for repeat in [1, 2]:
        result = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error',
                                 '-output-directory=' + str(build), str(tex)],
                                cwd=ROOT/folder, capture_output=True)
        (build/f'pass_{repeat}.txt').write_bytes(result.stdout + result.stderr)
        result.check_returncode()
    target = ROOT/output
    shutil.copyfile(build/'document.pdf', target)
    return dict(source=folder+'/'+source, output=output,
                source_sha256=hashlib.sha256((ROOT/folder/source).read_bytes()).hexdigest(),
                pdf_sha256=hashlib.sha256(target.read_bytes()).hexdigest())


if __name__ == '__main__':
    records = [compile_pdf('paper', 'manuscript_v4.md', 'submission_header.tex', 'paper/manuscript_v4_readable.pdf'),
               compile_pdf('supplement', 'validation_supplement.md', 'validation_header.tex', 'supplement/validation_supplement.pdf', True)]
    (ROOT/'docs/pdf_build.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    print('PASS: compiled manuscript and supplement PDFs in two passes each')
