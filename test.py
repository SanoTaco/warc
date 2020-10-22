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
]

total = {}
amount = {}
docT = {}
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

#print array

lentest = 0

dictTest = {}
#print doc_i
for s in range(np.shape(array)[0]):
    print array[s, 0]
    for v in array[s, 1]:
        if v not in dictTest:
            dictTest[v] = {}
        print "doc", int(v)+1, "\ttf:", len(array[s, 1][v])
        print "idf", np.log(doc_i/amount[array[s, 0]]+1)
        print "TF-IDF for doc", int(v)+1, ":", len(
            array[s, 1][v])*np.log(doc_i/amount[array[s, 0]]+1), "\n"
        tf_idf_data = len(array[s, 1][v])*np.log(doc_i/amount[array[s, 0]]+1)
        dictTest[v][array[s, 0]] = tf_idf_data


json_object = json.dumps(dictTest, indent=4)
print(json_object)
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
search_words = [x for x in wordlist if x in terms]

print "\nSearching for words: ", search_words, "\n"

doc_has_word = [(terms[word].keys(), word) for word in search_words]
doc_words = defaultdict(list)
for d, w in doc_has_word:
    for p in d:
        doc_words[p].append(w)

# create a dictionary identifying matches for each document

result_set = {}

for i in doc_words.keys():
    count = 0
    matches = len(doc_words[i])     # number of matches
    for w in doc_words[i]:
        count += len(terms[w][i])   # count total occurances
    result_set[i] = (matches, count)

# Now print in sorted order

print "<doc#>  \t <similarity score>"
print '-'*40
for doc, (matches, count) in sorted(result_set.items(), key=itemgetter(1), reverse=True):
    print doc, "  \t\t\t  ", count
