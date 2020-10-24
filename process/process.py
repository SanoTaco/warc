import warc
import gzip
import re 
from bs4 import BeautifulSoup
from collections import defaultdict
from string import digits
import numpy as np



def preProcessing(input_file):
    index = 1
    doc_total={}
    with open(input_file) as f:
        is_file = False
        content = ""
        for line in f.readlines():
            if "<html" in line:
                is_file = True
            if is_file:
                content = content + line
            if "</html" in line:
                is_file = False
                doc_total[index]=content
                #with open("output_htmls/"+str(index) + ".html", "w") as out:
                #    for l in content:
                #        out.write(l)
                index = index + 1
                content = ""
    # print dictList
    return index,doc_total

def parsing(index,doc_total):
    dictList = {}
    #print index
    for l in range(1,index):
        soup = BeautifulSoup(doc_total[l], 'lxml')
        for tag in soup(['script', 'style']):
            tag.extract()
        text = soup.get_text(separator=u'\n')
        text = text.strip()
        text = re.sub(r'[^\w]', '\n', text)
        text = re.sub(r'\n\s*\n', r'\n\n', text, flags=re.M)
        text = ''.join(i for i in text if not i.isdigit())
        text = ''.join([s for s in text.strip().splitlines(True) if s.strip("\r\n")])
        #print text
        text = text.lower().encode("utf-8")
        text = text.split("\n")
        #text = findValue(text,"\n")
        #text =tuple(text) 
        #dict2 = defaultdict(set)
        #dict2[l]=text
        word_dictionary = dict.fromkeys(text, "word")
        dictList[l]=word_dictionary
    #print dictList
    #print dictList
    return dictList

