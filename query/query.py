import math
import json
import random
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def query():
    docs_set = set()
    output_dict = {}
    term_index = {}
    query_table = {}
    docs_table={}
    query = raw_input("Query: ")
    if 'AND' in query:
        and_query = query.split("AND")
        and_query = str(and_query).replace("[", "").replace("]", "").replace(
            "'", "").replace(",", "").replace("AND", "")
        and_query = and_query.lower()
        and_query = and_query.strip()
        search_words = and_query.split()
    elif 'OR' in query:
        or_query = query.split("OR")
        query = random.choice(or_query)
        query = query.lower()
        query = query.strip()
        search_words = query.split()
    else:
        query = query.lower()
        query = query.strip()
        search_words = query.split()

    print "\nSearching for words: ", search_words, "\n"
    with open("page.total") as hama:
        N = hama.readline()
        N = int(N)

    with open("output.dict") as f:
        output_dict = json.load(f)

    print "\nDumping words to dict ...\n"
    
    for term in search_words:
        if term in output_dict:
            term_index[term] = output_dict[term]
            #print len(term_index[term])
            #print term_index
            for doc in term_index[term]:
                if str(doc)!="df":
                    docs_set.add(doc)
            #print docs_set
            query_table[term] = {}
            query_table[term]["tf"] = 1
            query_table[term]["df"] = len(term_index[term])
            query_table[term]["idf"] = math.log(
                N / query_table[term]["df"], 10)
            query_table[term]["w"] = (
                1 + math.log(query_table[term]["tf"])) * query_table[term]["idf"]
        else:
            term_index[term] = {}
            query_table[term] = {}
            query_table[term]["tf"] = 1
            query_table[term]["df"] = 0
            query_table[term]["idf"] = 0
            query_table[term]["w"] = 0
        
    while True:
        try:
            doc_id = str(docs_set.pop())
        except KeyError:
            break
        docs_table[doc_id] = {}
        for term in search_words:
            #print doc_id
            docs_table[doc_id][term] = {}
            docs_table[doc_id][term]["tf"] = 0
            if doc_id in term_index[term]:
                docs_table[doc_id][term]["tf"] = term_index[term][doc_id]["tf"]
    
    for doc_id in docs_table:
        for term in search_words:
            if docs_table[doc_id][term]["tf"] > 0:
                docs_table[doc_id][term]["w"] = (1 + math.log(docs_table[doc_id][term]["tf"], 10)) * math.log(
                    query_table[term]["df"], 10)
            else:
                docs_table[doc_id][term]["w"] = 0
    #print docs_table['24']
    docs_df = pd.DataFrame(docs_table)
    #query_df = pd.DataFrame(query_table)
    #query_w = query_df.loc['w'].values.tolist()
    print docs_df
    
    output_set={}
    for doc_id in docs_table:
        for term in search_words:
            #print list(query_table[term]["w"])
            #print docs_table[doc_id][term]["w"]

            output = str(cosine_similarity(q, d))
        #print temp


    