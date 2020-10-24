import numpy as np
import math
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
terms = {}
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["s", "is", "my", "sb", "student"],
    ["hama", "xp", "vista", "sb", "student"],
    ["brother", "who", "brother", "sb", "brother", "gg"]
]

terms_table = {}
query_table = {}
amount = {}
idf = {}
doc_i = 0
dictTest = {}
termsList = []

for v in test:
    for word in v:
        if word not in terms:
            terms[word] = {}
        if str(doc_i) not in terms[word]:
            terms[word][str(doc_i)] = {}
        terms[word][str(doc_i)] = [
            i for i, e in enumerate(v) if e == word]
    doc_i = doc_i+1

for word in terms:
    amount[word] = 0
    for docid in terms[word]:
        amount[word] = amount[word]+1

array = np.array(list(terms.items()))
for s in range(np.shape(array)[0]):
    termsList.append(array[s, 0])
    for v in array[s, 1]:
        if str(int(v)) not in dictTest:
            dictTest[str(int(v))] = {}
        if array[s, 0] not in idf:
            idf[array[s, 0]] = {}
        idf[array[s, 0]] = math.log10(doc_i/amount[array[s, 0]])
        tf_idf_data = (1+math.log10(len(array[s, 1][v]))) * \
            math.log10(doc_i/amount[array[s, 0]])
        if tf_idf_data > 0:
            dictTest[str(int(v))][array[s, 0]] = tf_idf_data
        else:
            dictTest[str(int(v))][array[s, 0]] = 0


for docid in dictTest:
    terms_table[docid] = {}
    for x in termsList:
        terms_table[docid][x] = 0
        if x in dictTest[docid].keys():
            terms_table[docid][x] = dictTest[docid][x]
print terms_table
query = raw_input("Query: ")
query = query.lower()
query = query.strip()
search_words = query.split()
for x in search_words:
    if x not in idf.keys():
        idf[x] = 0

for docid in terms_table:
    for x in search_words:
        if x not in termsList:
            terms_table[docid][x] = 0

for word in idf.keys():
    query_table[word] = 0
    if word in search_words:
        query_table[word] = idf[word]

print terms_table
print query_table

terms_set = pd.DataFrame(terms_table)
query_set = pd.DataFrame(query_table, index=terms_table.keys()).sort_index()
query_set = query_set[:1].values.tolist()

print "\nSearching for words: ", search_words, "\n"
print "<doc#>  \t <similarity score>"
print '-'*40

for docid in sorted(terms_table.keys()):
    temp = terms_set.loc[:, [docid]].values.tolist()
    temp_set =  str(temp).replace("[", "").replace("]", "")
    temp_set = temp_set.split(",")
    temp_set = map(float, temp_set)
    output = str(cosine_similarity(query_set, [temp_set]))
    print "  ",int(docid)+1, "\t\t\t", output.replace("[", "").replace("]", "")
