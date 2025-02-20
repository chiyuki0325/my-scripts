from pathlib import Path
import sys
from xml.dom.minidom import (
    parse as parse_xml,
    Element
) 
import os
from subprocess import run,PIPE

folder = Path(sys.argv[1])

def extract_title(el: Element):
    try:
        return el.childNodes[0].data
    except Exception:
        return ''
    
def convert(file):
    document = parse_xml(open(file)).documentElement
    title_els = document.getElementsByTagName('h1')
    title_els.extend(document.getElementsByTagName('h2'))
    title_els.extend(document.getElementsByTagName('h3'))
    titles = map(extract_title, title_els)
    title_str = str(''.join(list(filter(str.isdigit, file.name)))) + ': ' +  ' - '.join(list(filter(lambda part: part != '',titles)))
    this_content = run([
        'pandoc', '-f', 'html', file, '-t', 'plain', 
    ], stdout=PIPE, stderr=PIPE, check=True).stdout.decode('utf-8').replace('\n\n', '\n')
    if len(title_str) > 40:
        title_str = title_str[:40]
    open(folder / (title_str + '.txt'), 'w').write(this_content)


for html_file in folder.glob("**/*.html"):
    convert(html_file)
for xhtml_file in folder.glob("**/*.xhtml"):
    convert(xhtml_file)