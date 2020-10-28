import math
import json
import random
import sys
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def query():
    docs_set = set()
    output_dict = {}
    term_index = {}
    query_table = {}
    docs_table = {}
    docs_score = {}
    query = raw_input("Query: ")
    query = query.lower()
    query = query.strip()
    search_words = query.split()
    return_count = 10
    return_count = int(raw_input("K (how many document may display): "))

    print "Searching for words: ", search_words
    with open("page.total") as hama:
        N = hama.readline()
        N = int(N)

    print "Loading dict ..."
    with open("output.dict") as f:
        output_dict = json.load(f)

    print "Dumping words to dict ..."

    for term in search_words:
        if term in output_dict:
            term_index[term] = output_dict[term]
            #print len(term_index[term])
            #print term_index
            for doc in term_index[term]:
                if str(doc) != "df":
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

    euclidean_length = 0
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
            euclidean_length += docs_table[doc_id][term]["tf"] * \
                docs_table[doc_id][term]["tf"]
    euclidean_length = math.sqrt(euclidean_length)

    for doc_id in docs_table:
        for term in search_words:
            if docs_table[doc_id][term]["tf"] > 0:
                docs_table[doc_id][term]["w"] = (1 + math.log(docs_table[doc_id][term]["tf"], 10)) * math.log(
                    query_table[term]["df"], 10)
            else:
                docs_table[doc_id][term]["w"] = 0

    query_len = 0
    for term in search_words:
        query_len += query_table[term]["w"] * query_table[term]["w"]
    query_len = math.sqrt(query_len)

    for doc in docs_table:
        up_part = 0
        doc_len = 0
        for terms in search_words:
            up_part += docs_table[doc][terms]["w"] * query_table[terms]["w"]
            doc_len += docs_table[doc][terms]["w"] * \
                docs_table[doc][terms]["w"]
        docs_score[doc] = up_part / (math.sqrt(doc_len) * query_len)
    print "Top", return_count, "results:"
    print "doc#\tsimilarity score"
    for i in sorted(docs_score, key=docs_score.get, reverse=True):
        return_count -= 1
        if return_count < 0:
            break
        print("%d\t%.3f" % (int(i), docs_score[i]))


def query_bs():
    print "Write Boolean Search here!"
