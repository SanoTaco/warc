import json
import numpy as np
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter
import math

terms = {}
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["s", "is", "my", "sb", "student"],
    ["s", "sb", "sb", "sb", "student"],
    ["brother", "who", "brother", "sb", "brother", "gg"]
    #["brother", "who", "brother", "sb", "brother", "gg"]
]

terms_table = {}
amount = {}
idf = {}
doc_i = 0

a = ""
for v in test:
    for word in v:
        if word not in terms:
            terms[word] = {}
        if str(doc_i) not in terms[word]:
            terms[word][str(doc_i)] = {}
            # terms[word]["tf"]=0
        terms[word][str(doc_i)] = [
            i for i, e in enumerate(v) if e == word]
        # terms[word]["tf"]=terms[word]["tf"]+1
        #print terms[word].keys(), terms.keys(), terms[word]
    doc_i = doc_i+1


for word in terms:
    amount[word] = 0
    for docid in terms[word]:
        amount[word] = amount[word]+1

print amount["brother"]

#names = ['id','data']
#formats = ['f8','f8']
#dtype = dict(names = names, formats=formats)
array = np.array(list(terms.items()))

print array[0][0]

lentest = 0

dictTest = {}
queryTest=[]
#print doc_i
termsList=[]

for s in range(np.shape(array)[0]):
    print array[s, 0]
    termsList.append(array[s, 0])
    for v in array[s, 1]:
        if "doc"+str(int(v)+1) not in dictTest:
            dictTest["doc"+str(int(v)+1)] = {}
            #idf[array[s, 0]]={}
        #if array[s, 0] not in idf:
            #idf[array[s, 0]]={}
        print "doc", int(v)+1, "\ttf:", len(array[s, 1][v])
        print "idf", np.log(doc_i/amount[array[s, 0]]+1)
        #idf[array[s, 0]]=np.log(doc_i/amount[array[s, 0]]+1)
        print "TF-IDF for doc", int(v)+1, ":", (1+np.log(len(array[s, 1][v])))*np.log10(doc_i/amount[array[s, 0]]+1), "\n"
        tf_idf_data = (1+np.log(len(array[s, 1][v])))*np.log10(doc_i/amount[array[s, 0]]+1)
        if tf_idf_data>0:
            dictTest["doc"+str(int(v)+1)][array[s, 0]] = tf_idf_data
        else:
            dictTest["doc"+str(int(v)+1)][array[s, 0]] = 0


for docid in dictTest:
    terms_table[docid]={}
    for x in termsList:
        terms_table[docid][x]=0
        if x in dictTest[docid].keys():
            terms_table[docid][x]=dictTest[docid][x]
#print terms_table

json_object = json.dumps(terms_table, indent=4,sort_keys=True)
print(json_object)

#json_object1 = json.dumps(idf, indent=4,sort_keys=True)
##print(json_object1)
# for docNumber in dictTest:
#    for data in dictTest[docNumber]:
#        print docNumber, data, dictTest[docNumber][data]

query = raw_input("Query: ")

# Some preprocessing

query = query.lower()
query = query.strip()

# now real work

wordlist = query.split()
# list of words that are present in index.
search_words = [x for x in wordlist if x in idf]

print "\nSearching for words: ", search_words, "\n"


#for i in search_words:
#    for s in range(np.shape(array)[0]):




print "<doc#>  \t <similarity score>"
print '-'*40