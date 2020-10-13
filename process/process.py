import warc
import gzip
import re
import os
import shutil

from bs4 import BeautifulSoup
from string import digits

path = 'output_htmls'
pathDoc = 'document'
if not os.path.exists(path):
    os.makedirs(path)
elif not os.path.exists(pathDoc):
    os.makedirs(pathDoc)

def preProcessing(content):
    with open(content) as f:
        is_file = False
        content = ""
        index = 1
        for line in f.readlines():
            if "<html" in line:
                is_file = True
            if is_file:
                content = content + line
            if "</html" in line:
                is_file = False
                with open("output_htmls/"+str(index) + ".html", "w") as out:
                    for l in content:
                        out.write(l)
                soup = BeautifulSoup(
                    open('output_htmls/'+str(index) + '.html'), 'lxml')
                for tag in soup(['script', 'style']):
                    tag.extract()
                text = soup.get_text(separator=u'\n')
                text = text.strip()
                text = re.sub(r'[^\w]', '\n', text)
                text = re.sub(r'\n\s*\n', r'\n\n', text, flags=re.M)
                text = ''.join(i for i in text if not i.isdigit())
                text = ''.join(
                    [s for s in text.strip().splitlines(True) if s.strip("\r\n")])
                with open("document/"+"doc"+str(index), "w") as out:
                    for l in text.split('\n'):
                        if l != '\n':
                            out.write(l+'\n')
                index = index + 1
                content = ""
    shutil.rmtree(path)