import json
import numpy as np
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter

terms = {}
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["brother", "is", "my", "sb", "student"],
    ["brother", "sb", "sb", "sb", "student"]
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
        terms[word][str(doc_i)] = [
            i for i, e in enumerate(v) if e == word]
       # terms[word][str(doc_i)]["tf"]=terms[word][str(doc_i)]["tf"]+1
        #print terms[word].keys(), terms.keys(), terms[word]
    doc_i = doc_i+1

for word in terms:
    amount[word] = 0
    for docid in terms[word]:
        amount[word] = amount[word]+len(terms[word][docid])


#names = ['id','data']
#formats = ['f8','f8']
#dtype = dict(names = names, formats=formats)
array = np.array(list(terms.items()))

print array[3,0], "\n\t\n",array[3, 1].keys()

lentest=0

for v in array[3, 1]:
    print array[3, 1][v]
    lentest = lentest+len(array[3, 1][v])
print lentest

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
