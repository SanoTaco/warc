import json
import numpy as np
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter

terms = {}
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["brother", "is", "my", "a", "student"]
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
        print terms[word].keys(),terms.keys()
    doc_i = doc_i+1

for word in terms:
    amount[word] = 0
    for docid in terms[word]:
        amount[word] = amount[word]+len(terms[word][docid])


    #print testOutput


#print(sorted(terms.items(), key=lambda obj: obj[0]))
json_object = json.dumps(terms, indent=2)
print(json_object)
output = "\n".join("{}\t{}".format(k, v) for k, v in terms.items())
output.replace("{", "<")
output.replace("}", ">")
# output1= "\n".join("{}\t{}".format(k, v) for k, v in totalTerms.items())
# print output
# print output
f = open("outtestsbput.dict", "w")
f.write(output)
f.close()
# print terms.items()

# Take input

query = raw_input(" Enter the query : ")

# Some preprocessing

query = query.lower()
query = query.strip()

# now real work

wordlist = query.split()
search_words = [ x for x in wordlist if x in terms ]    # list of words that are present in index.

print ("\nsearching for words ... : ", search_words, "\n")

doc_has_word = [ (terms[word].keys(),word) for word in search_words ]
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
    result_set[i] = (matches,count)

# Now print in sorted order

print ("   Document \t\t Words matched \t\t Total Frequency ")
print ('-'*40)
for doc, (matches, count) in sorted(result_set.items(), key = itemgetter(1), reverse = True):
    print (doc, "\t",doc_words[doc],"\t",count)