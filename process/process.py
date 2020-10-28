import warc
import gzip
import re
import time
from bs4 import BeautifulSoup
from collections import defaultdict
from string import digits


def preProcessing(input_file):
    url_dict = {}
    f = warc.open(input_file, "rb")
    for record in f:
        if record['Warc-type'] == 'warcinfo':
            pass
        else:
            str_test = str(record.payload)
            url_dict[record['WARC-Record-ID']] = str_test
    return url_dict


def crash_clean(html_text):
    # discard html headers
    html_text = re.sub('^HTTP[^<]*<', '<', html_text, flags=re.DOTALL)

    # discard possible comments in raw html
    html_text = re.sub(r'<!--(.*?)-->', ' ', html_text, flags=re.DOTALL)

    # Since new line feeds in HTML have no use,
    # remove all new lines in the original text before we do,
    # because we will use the line feed as separator for differenct sentences.
    html_text = re.sub(r'[\r\n]+', ' ', html_text, flags=re.DOTALL)
    html_text = re.sub(r'  +', ' ', html_text, flags=re.DOTALL)

    return html_text


def not_empty(s):
    return s and s.strip()

#res = filter(not_empty, ['1', '', '2', None, '3', '  '])


def parsing(index):
    #tStart = time.time()
    dictList = []
    for l in index:
        soup = BeautifulSoup(crash_clean(index[l]), 'lxml')
        for tag in soup(['script', 'style']):
            tag.extract()
        text = soup.get_text(separator=u'\n')
        text = text.replace("_", "\n")
        text = text.strip()
        text = re.sub(r'[^\w]', '\n', text)
        text = re.sub(r'[^\w]', '\n', text)
        text = re.sub(r'\n\s*\n', r'\n\n', text, flags=re.M)
        text = ''.join(i for i in text if not i.isdigit())
        text = ''.join(
            [s for s in text.strip().splitlines(True) if s.strip("\r\n")])
        text = text.lower().encode("utf-8")
        text = text.split("\n")
        text = filter(not_empty, text)
        dictList.append(text)
        #print str(l)+" has been done ."
    #tEnd = time.time()
    #print ("Parsing cost %f sec" % (tEnd - tStart))
    return dictList
