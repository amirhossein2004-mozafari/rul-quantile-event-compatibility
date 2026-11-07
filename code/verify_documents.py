"""Check rendered prose, table numbers and supplement cross-references."""
import collections
import json
import re
import subprocess
import unicodedata
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def normalize(text):
    return ''.join(char.lower() for char in unicodedata.normalize('NFKC', unquote(text)) if char.isalnum())


def main():
    md = (ROOT/'paper/manuscript_v4.md').read_text(encoding='utf-8')
    pdf = subprocess.check_output(['pdftotext', '-layout', str(ROOT/'paper/manuscript_v4_readable.pdf'), '-'], encoding='utf-8').replace('\f', '\n')
    pdf = re.sub(r'(?m)^ *Quantile and event-probability compatibility +A\. H\. Mozafari *$', '', pdf)
    pdf = re.sub(r'(?m)^ *Necessary compatibility diagnostic +\d+ *$', '', pdf)
    pdf = re.sub(r'(?m)^ {0,5}\d+ {3}', '', pdf)
    pdf = re.sub(r'(?m)^ +\d+ *$', '', pdf)
    ast = json.loads(subprocess.check_output(['pandoc', 'manuscript_v4.md', '--citeproc', '--bibliography=references.bib', '-t', 'json'], cwd=ROOT/'paper', encoding='utf-8'))
    blocks = []

    def walk(items):
        for block in items:
            if block['t'] in ['Para', 'Plain', 'Header']:
                blocks.append(block)
            elif block['t'] == 'Div':
                walk(block['c'][1])
            elif block['t'] == 'BlockQuote':
                walk(block['c'])

    walk(ast['blocks'])
    missing = []
    for number, block in enumerate(blocks):
        single = dict(ast, blocks=[block])
        plain = subprocess.check_output(['pandoc', '-f', 'json', '-t', 'plain', '--wrap=none'], input=json.dumps(single), encoding='utf-8').strip()
        if normalize(plain) not in normalize(pdf):
            missing.append(dict(block=number, text=plain))
    groups = [[line for line in block.splitlines() if line.startswith('| FD')] for block in md.split('\n\n') if block.startswith('|') and '| FD' in block]
    numbers = lambda text: re.findall(r'(?<![\w.])-?\d+(?:\.\d+)?', text.replace('−', '-'))
    table_issues = []
    rows_checked = 0
    for index, rows in enumerate(groups, 1):
        start = pdf.index('Table ' + str(index) + ':')
        end = pdf.find('Table ' + str(index+1) + ':', start+1) if index < 4 else pdf.index('5. Limitations', start)
        region = pdf[start:end]
        if index == 1:
            region = region[:region.index('The pooled RUL-only Brier coefficient')]
        if index == 2:
            region = region[:region.index('4. Secondary calibration')]
        if index == 3:
            region = region[:region.index('Table 4 shows the four')]
        starts = list(re.finditer(r'(?m)^\s*FD00[1-4]\s+(?:lstm|hybrid|LSTM|Hybrid)', region))
        assert len(starts) == len(rows), (index, len(starts), len(rows))
        for row_index, (row, match) in enumerate(zip(rows, starts)):
            segment = region[match.start():starts[row_index+1].start() if row_index+1 < len(starts) else len(region)]
            missing_numbers = collections.Counter(numbers(row)) - collections.Counter(numbers(segment))
            rows_checked += 1
            if missing_numbers:
                table_issues.append(dict(table=index, row=row_index+1, missing=list(missing_numbers.elements())))
    supplement = (ROOT/'supplement/validation_supplement.md').read_text(encoding='utf-8')
    heads = '\n'.join(line for line in supplement.splitlines() if line.startswith('#'))
    labels = set(re.findall(r'\bS(?:1[0-4]|[0-9])(?:[a-z])?\b', heads))
    main_refs = set(re.findall(r'\bS(?:1[0-4]|[0-9])(?:[a-z])?\b', md))
    unresolved = sorted(label for label in main_refs if label not in labels and not any(item.startswith(label) for item in labels))
    base_numbers = {int(re.match(r'S(\d+)', label).group(1)) for label in labels}
    assert set(range(15)).issubset(base_numbers)
    supp_pdf = subprocess.check_output(['pdftotext', '-layout', str(ROOT/'supplement/validation_supplement.pdf'), '-'], encoding='utf-8')
    absent_pdf_labels = sorted(label for label in labels if label not in supp_pdf)
    report = dict(prose_blocks_checked=len(blocks), missing_prose=missing, main_table_rows_checked=rows_checked,
                  table_issues=table_issues, supplement_families=list(range(15)), main_supplement_references=sorted(main_refs),
                  unresolved_supplement_references=unresolved, supplement_labels_absent_from_pdf=absent_pdf_labels,
                  scope='Prose normalized for line numbers, page furniture and typography; table numeric tokens checked by row. Table renderer independently matches all displayed cells from CSVs. Visual review is separate.')
    report['status'] = 'PASS' if not (missing or table_issues or unresolved or absent_pdf_labels) else 'FAIL'
    (ROOT/'docs/document_verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({key: value for key, value in report.items() if key not in ['scope', 'main_supplement_references']}, indent=2))
    assert report['status'] == 'PASS'


if __name__ == '__main__':
    main()
