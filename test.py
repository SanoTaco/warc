import json
import numpy as np
from collections import OrderedDict
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
        terms[word][str(doc_i)]["pos"] = [
            i for i, e in enumerate(v) if e == word]
       # terms[word][str(doc_i)]["tf"]=terms[word][str(doc_i)]["tf"]+1
    doc_i = doc_i+1

for word in terms:
    amount[word] = 0
    for docid in terms[word]:
        for pos in terms[word][docid]:
            amount[word] = amount[word]+len(terms[word][docid][pos])

for word in terms:
    testOutput = word+","+str(amount[word])+":\n<"
    for docid in terms[word]:
        for pos in terms[word][docid]:
            testOutput = testOutput+"doc"+str(int(docid))+","
            testOutput = testOutput+str(len(terms[word][docid][pos]))+":<"+str(
                terms[word][docid][pos]).replace("[", "").replace("]", "")+">;"
    testOutput = testOutput+">"
    print testOutput


#print(sorted(terms.items(), key=lambda obj: obj[0]))
json_object = json.dumps(terms, indent=2)
# print(json_object)
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
