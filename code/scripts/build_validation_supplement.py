"""Checked PDF compilation of the validation document only."""
from pathlib import Path
import subprocess,shutil,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'paper';B=ROOT/'tmp/manuscript_build'
(B/'validation_landscape_header.tex').write_text(chr(92)+'usepackage{pdflscape}\n',encoding='utf-8')
command=['pandoc','validation_supplement.md','--standalone','--resource-path=.','--include-in-header=validation_header.tex','--include-in-header='+str(B/'validation_landscape_header.tex'),'-V','geometry:margin=0.75in','-V','fontsize=10pt','-V','papersize=a4','-V','mainfont=Times New Roman','-V','sansfont=Arial','-V','monofont=Consolas','-o',str(B/'validation_supplement.tex')]
with (B/'validation_pandoc.log').open('w',encoding='utf-8') as log:subprocess.run(command,cwd=P,stdout=log,stderr=subprocess.STDOUT,check=True)
tex=B/'validation_supplement.tex'
source=tex.read_text(encoding='utf-8')
source=re.sub(r'\\texttt\{([0-9a-f]{64})\}',lambda m:r'\texttt{\seqsplit{'+m.group(1)+'}}',source)
tex.write_text(source,encoding='utf-8')
for repeat in [1,2]:
    with (B/f'validation_checked_{repeat}.log').open('w',encoding='utf-8') as log:subprocess.run(['xelatex','-interaction=nonstopmode','-halt-on-error',f'-output-directory={B}',str(B/'validation_supplement.tex')],cwd=P,stdout=log,stderr=subprocess.STDOUT,check=True)
shutil.copy2(B/'validation_supplement.pdf',P/'validation_supplement.pdf')
print('Validation supplement compiled successfully (two checked passes).')
