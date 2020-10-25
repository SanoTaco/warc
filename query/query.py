
import numpy as np
import math
import json
import random
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def query():
    terms_table = {}
    query_table = {}
    temp_table = {}
    idf = {}
    df={}
    termsList = []
    doc_i=0

    with open("page.total") as hama:
        doc_i=hama.readline()

    with open("output.dict") as f:
        text= json.load(f)

    doc_i=int(doc_i)
    
    for word in text:
        if word not in idf:
            idf[word]=0
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
    
    query = raw_input("Query: ")
    if 'AND' in query:
        and_query = query.split("AND")
        and_query = str(and_query).replace("[","").replace("]","").replace("'","").replace(",","").replace("AND","")
        #print and_query
        and_query = and_query.lower()
        and_query = and_query.strip()
        search_words = and_query.split()
    elif 'OR' in query:
        or_query= query.split("OR")
        #print or_query
        query=random.choice(or_query)
        query = query.lower()
        query = query.strip()
        search_words = query.split()
        #search_words=random.choice(search_words)
    else:
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
    print ("\nSearching for words: ", search_words, "\n")
    #print "<doc#>  \t <similarity score>"
    #print '-'*40
    for docid in sorted(terms_table.keys()):
        temp = terms_set.loc[:, [docid]].values.tolist()
        temp_set =  str(temp).replace("[", "").replace("]", "")
        temp_set = temp_set.split(",")
        temp_set = map(float, temp_set)
        output = str(cosine_similarity(query_set, [temp_set])).replace("[", "").replace("]", "")
        output=float(output)
        output_set[docid]=output
        #print "  ",int(docid)+1, "\t\t\t", output

    output_df= pd.DataFrame(output_set.items(),columns=['doc#','similarity score'])
    #output_df.drop(output_df.columns[0],axis=1,inplace=True)
    print (output_df.sort_values(by='similarity score', ascending=False).to_string(index=False))