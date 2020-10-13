import warc
import gzip
import re


from bs4 import BeautifulSoup
from string import digits

globalI=0
total_dict={}
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
                text = text.lower()
                with open("document/"+"doc"+str(index), "w") as out:
                    for l in text:
                        #if l != '\n':
                        out.write(l)
                index = index + 1
                globalI=index
                content = ""
    word_dict = {}
    with open("document/doc1",'r') as fp:
        for index,word in enumerate(fp):
            if word not in word_dict:
                word = re.sub('\n+', '\n', word)
                #print word
                word_dict[word]=[index+1]
            else:
                word_dict[word].append(index+1)
    word_dict = {x.replace('\n', ''): v for x, v in word_dict.items()} 
    for key,value in word_dict.items():
        print('{key},{value}'.format(key = key, value = value)+","+str(len(value)))
        #print(len(value))
 
