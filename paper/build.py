"""Build the supplied-class IJPHM manuscript; no analysis or model execution."""
from pathlib import Path
import os
import re
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
BUILD = HERE / '.build'
BUILD.mkdir(exist_ok=True)

def run(command, cwd, name, env=None):
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True)
    (BUILD/name).write_bytes(result.stdout + result.stderr)
    if result.returncode:
        print((result.stdout+result.stderr).decode('utf-8', errors='replace')[-7000:])
        result.check_returncode()

command = ['xelatex', '-interaction=nonstopmode', '-halt-on-error',
           '-output-directory='+str(BUILD), 'manuscript.tex']
env = os.environ.copy()
env['TEXINPUTS'] = str(BUILD/'dependencies')+os.pathsep+env.get('TEXINPUTS', '')
run(command, HERE, 'pass_1.txt', env)
env['BIBINPUTS'] = str(HERE)+os.pathsep+env.get('BIBINPUTS', '')
run(['bibtex', 'manuscript'], BUILD, 'bibtex.txt', env)
shutil.copyfile(BUILD/'manuscript.bbl', HERE/'manuscript.bbl')
run(command, HERE, 'pass_2.txt', env)
run(command, HERE, 'pass_3.txt', env)
log = (BUILD/'manuscript.log').read_text(encoding='utf-8', errors='replace')
warnings = re.findall(r'Overfull \\[hv]box[^\n]*', log)
shutil.copyfile(BUILD/'manuscript.pdf', HERE/'manuscript.pdf')
shutil.copyfile(BUILD/'manuscript.bbl', HERE/'manuscript.bbl')
print('Built manuscript.pdf with official class, XeLaTeX and APA BibTeX.')
print('Overfull boxes:', len(warnings))
for warning in warnings:
    print(warning)
if re.search(r'Citation .* undefined|There were undefined references|Missing character:', log):
    raise SystemExit('Unresolved citation/reference or missing glyph: inspect .build/manuscript.log')
if warnings:
    raise SystemExit('Layout needs adjustment: overfull boxes remain')
