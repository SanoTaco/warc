import math
import json
import random
import sys


def query():
    docs_list = []
    output_dict = {}
    term_index = {}
    query_table = {}
    docs_table = {}
    docs_score = {}
    query_len = 0
    query = raw_input("Query: ")
    query = query.lower()
    query = query.strip()
    search_words = query.split()
    ret_k = 10
    ret_k = int(raw_input("K (how many document may display): "))

    print "Searching for words: ", search_words
    with open("page.total") as page:
        N = page.readline()
        N = int(N)

    print "Loading dict ..."
    with open("output.dict") as f:
        output_dict = json.load(f)

    print "Dumping words to dict ..."

    for term in search_words:
        if term in output_dict:
            term_index[term] = output_dict[term]
            for doc in term_index[term]:
                if str(doc) != "df":
                    docs_list.append(doc)
            query_table[term] = {}
            query_table[term]["tf"] = 1
            query_table[term]["df"] = len(term_index[term])
            query_table[term]["idf"] = math.log10(
                N / query_table[term]["df"])
            query_table[term]["w"] = (
                1 + math.log(query_table[term]["tf"])) * query_table[term]["idf"]
        else:
            term_index[term] = {}
            query_table[term] = {}
            query_table[term]["tf"] = 1
            query_table[term]["df"] = 0
            query_table[term]["idf"] = 0
            query_table[term]["w"] = 0

    for doc_id in docs_list:
        docs_table[doc_id] = {}
        for term in search_words:
            docs_table[doc_id][term] = {}
            docs_table[doc_id][term]["tf"] = 0
            if doc_id in term_index[term]:
                docs_table[doc_id][term]["tf"] = term_index[term][doc_id]["tf"]

    for doc_id in docs_table:
        for term in search_words:
            if docs_table[doc_id][term]["tf"] > 0:
                docs_table[doc_id][term]["w"] = (1 + math.log10(docs_table[doc_id][term]["tf"])) * math.log10(
                    query_table[term]["df"])
            else:
                docs_table[doc_id][term]["w"] = 0

    for term in search_words:
        query_len += query_table[term]["w"] * query_table[term]["w"]

    for doc_id in docs_table:
        up = 0
        down = 0
        doc_len = 0
        for terms in search_words:
            up += docs_table[doc_id][terms]["w"] * query_table[terms]["w"]
            doc_len += docs_table[doc_id][terms]["w"] * \
                docs_table[doc_id][terms]["w"]
            down = math.sqrt(doc_len) * math.sqrt(query_len)
        docs_score[doc_id] = up / down
    print "Top", ret_k, "results:"
    print "doc#\tsimilarity score"
    for i in sorted(docs_score, key=docs_score.get, reverse=True):
        ret_k -= 1
        if ret_k < 0:
            break
        print("%d\t%.3f" % (int(i), docs_score[i]))