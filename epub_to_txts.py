from pathlib import Path
import sys
from xml.dom.minidom import (
    parse as parse_xml,
    Element
)
from subprocess import run,PIPE

index_path, content_folder, output_folder = sys.argv[1], sys.argv[2], sys.argv[3]
content_folder = Path(content_folder)
output_folder = Path(output_folder)
output_folder.mkdir(parents=True, exist_ok=True)

index_document: Element = parse_xml(open(index_path)).documentElement

for para_node in index_document.getElementsByTagName('div'):
    if para_node.getAttribute("class") == 'kindle-cn-toc-level-1':
        para_title = ''
        for sub_node in para_node.childNodes:
            if isinstance(sub_node, Element):
                match sub_node.tagName:
                    case 'a':
                        para_title = sub_node.childNodes[0]
                        if para_title.nodeType == para_title.TEXT_NODE:
                            para_title = para_title.data
                        else:
                            para_title = para_title.childNodes[0].data
                    case 'div':
                        if sub_node.getAttribute('class') == 'kindle-cn-toc-level-2':
                            a_node = sub_node.getElementsByTagName('a')[0]
                            article_name: str = a_node.childNodes[0].data
                            article_path: str = a_node.getAttribute('href')
                            print(f'{para_title} / {article_name}')
                            this_content = run([
                                'pandoc', '-f', 'html', (content_folder / Path(article_path).name), '-t', 'plain', 
                            ], stdout=PIPE, stderr=PIPE, check=True).stdout.decode('utf-8').replace('\n\n', '\n')
                            output_article_path = output_folder / para_title / (article_name + '.txt')
                            output_article_path.parent.mkdir(parents=True, exist_ok=True)
                            with open(output_article_path, 'w') as f:
                                f.write(f"{para_title} - {article_name}\n\n")
                                f.write(this_content)
