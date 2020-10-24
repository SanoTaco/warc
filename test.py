import json
import numpy as np
from collections import OrderedDict
from collections import defaultdict
from operator import itemgetter
import math
import pandas as pd
terms = {}
terms_table = {}
temp_table = {}
test = [
    ["brother", "brother", "is", "my", "brother"],
    ["s", "is", "my", "sb", "student"],
    ["hama", "xp", "vista", "sb", "student"],
    ["brother", "who", "brother", "sb", "brother", "gg"]
]

terms_table = {}
amount = {}
termsList=[]
idf = {}
df={}
doc_i = 0
test_dict={}
a = ""
finalOutput="{\n"
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

for word in sorted(terms):
    testOutput ="'" +word+"':{'df':"+str(amount[word])+","
    for docid in sorted(terms[word]):
        testOutput = testOutput+"'doc"+str(int(docid)+1)+"':{'tf':"+str(len(terms[word][docid]))+","
        testOutput = testOutput+"'pos':"+str(terms[word][docid])+"},"
    testOutput = testOutput+"},"
    testOutput = list(testOutput)
    testOutput[len(testOutput)-3]=''
    finalOutput = finalOutput + ''.join(testOutput)+"\n"

finalOutput =list(finalOutput)
finalOutput[len(finalOutput)-2]=''
realfinal= ''.join(finalOutput)+'}'
realfinal=realfinal.replace( "'", '"' ).encode("utf-8")
#print realfinal

f = open("realfinal.json", "w")
f.write(realfinal)
f.close()

text = json.loads(realfinal)
for word in text:
    if word not in idf:
        idf[word]={}
    termsList.append(word)
    for docid in text[word]:
        if str(docid) == "df":
            df[word]=text[word][docid]
            idf[word]=math.log10(doc_i/df[word])
        else:
            if docid not in temp_table:
                temp_table[docid]={}
            for name in text[word][docid]:
                if str(name) == "tf":
                    tf_idf_data = (1+math.log(text[word][docid][name])) * idf[word]
                    if tf_idf_data > 0:
                        temp_table[docid][word] = tf_idf_data
                    else:
                        temp_table[docid][word] = 0




for docid in temp_table:
        terms_table[docid] = {}
        for x in termsList:
            terms_table[docid][x] = 0
            if x in temp_table[docid].keys():
                terms_table[docid][x] = temp_table[docid][x]
terms_set = pd.DataFrame(terms_table)
query_set = pd.DataFrame(query_table, index=terms_table.keys()).sort_index()
query_set = query_set[:1].values.tolist()
output_set={}
print "\nSearching for words: ", search_words, "\n"
    #print "<doc#>  \t <similarity score>"
    #print '-'*40
for docid in sorted(terms_table.keys()):
        temp = terms_set.loc[:, [docid]].values.tolist()
        temp_set =  str(temp).replace("[", "").replace("]", "")
        temp_set = temp_set.split(",")
        temp_set = map(float, temp_set)
        output = str(cosine_similarity(query_set, [temp_set])).replace("[", "").replace("]", "")
        output=float(output)
        output_set[int(docid)+1]=output
        #print "  ",int(docid)+1, "\t\t\t", output    

output_df= pd.DataFrame(output_set.items(),columns=['doc#','similarity score'])
    #output_df.drop(output_df.columns[0],axis=1,inplace=True)
print output_df.sort_values(by='similarity score', ascending=False).to_string(index=False)