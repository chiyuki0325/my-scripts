from pathlib import Path
import sys
from xml.dom.minidom import (
    parse as parse_xml,
    Element
) 
import os
from subprocess import run,PIPE

folder = Path(sys.argv[1])

def convert(file):
    document = parse_xml(open(file)).documentElement
    title = document.getElementsByTagName('h1')[0].childNodes[0].data
    this_content = run([
        'pandoc', '-f', 'html', file, '-t', 'plain', 
    ], stdout=PIPE, stderr=PIPE, check=True).stdout.decode('utf-8').replace('\n\n', '\n')
    open(folder / (title + '.txt'), 'w').write(this_content)


for html_file in folder.glob("**/*.html"):
    convert(html_file)
for xhtml_file in folder.glob("**/*.xhtml"):
    convert(xhtml_file)