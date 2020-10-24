import warc
import gzip
import re
from bs4 import BeautifulSoup
from string import digits

def preProcessing(input_file):
    dictList = []
    with open(input_file) as f:
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
                text = text.lower().encode("utf-8")
                text = text.split("\n")
                dictList.append(text)
                index = index + 1
                content = ""
    # print dictList
    return dictList
