import warc
import gzip
import re 
from bs4 import BeautifulSoup
from collections import defaultdict
from string import digits
from lxml import etree
import requests
def preProcessing(input_file):
    #index = 1
    #doc_total={}
    url_dict={}
    f = warc.open(input_file, "rb")
    for record in f:
        if record['Warc-type'] == 'warcinfo':
            pass
        else:
            str_test=str(record.payload)
            #hama=str_test.index(" ")
            #print hama
            url_dict[record['WARC-Record-ID']]=str_test
            #index=index+1
    #print url_dict['<urn:uuid:721f9a28-6b9a-44c1-bccd-8c7accb514cd>']
    #print index
    return url_dict

def crash_clean(html_text):
    # discard html headers
    html_text = re.sub('^HTTP[^<]*<', '<', html_text, flags=re.DOTALL)

    # discard possible comments in raw html
    html_text = re.sub(r'<!--(.*?)-->', ' ', html_text, flags=re.DOTALL)

    # Since new line feeds in HTML have no use, 
    # remove all new lines in the original text before we do,
    # because we will use the line feed as separator for differenct sentences.
    html_text = re.sub(r'[\r\n]+', ' ', html_text)
    html_text = re.sub(r'  +', ' ', html_text)

    return html_text

def parsing(index):
    dictList = {}
    #print index
    for l in index:
        #r = requests.get(index[l])
        soup = BeautifulSoup(crash_clean(index[l]), 'lxml')
        for tag in soup(['script', 'style']):
            tag.extract()
        text = soup.get_text(separator=u'\n')
        #print text
        #html = etree.parse(doc_total[l], etree.HTMLParser())
        #result = html.xpath('//html//*')
        #print(result)
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

