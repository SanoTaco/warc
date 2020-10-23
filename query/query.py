
import numpy as np
import math
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def query(terms_file, amount_file, total):
    terms_table = {}
    query_table = {}
    temp_table = {}
    idf = {}
    termsList = []

    array = np.array(list(terms_file.items()))
    for s in range(np.shape(array)[0]):
        termsList.append(array[s, 0])
        for v in array[s, 1]:
            if str(int(v)) not in temp_table:
                temp_table[str(int(v))] = {}
            if array[s, 0] not in idf:
                idf[array[s, 0]] = {}
            idf[array[s, 0]] = math.log(total/amount_file[array[s, 0]]+1)
            tf_idf_data = (1+math.log(len(array[s, 1][v]))) * \
                math.log10(total/amount_file[array[s, 0]]+1)
            if tf_idf_data > 0:
                temp_table[str(int(v))][array[s, 0]] = tf_idf_data
            else:
                temp_table[str(int(v))][array[s, 0]] = 0

    for docid in temp_table:
        terms_table[docid] = {}
        for x in termsList:
            terms_table[docid][x] = 0
            if x in temp_table[docid].keys():
                terms_table[docid][x] = temp_table[docid][x]

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