#import pprint

terms = {}

def indexing(dictList):  
    doc_i = 0
    for v in dictList:
        for word in v:
            if word not in terms:
                terms[word] = {}
            if str(doc_i) not in terms[word]:
                terms[word][str(doc_i)] = 0
            terms[word][str(doc_i)] = terms[word][str(doc_i)] + 1
        doc_i = doc_i+1
    #pp = pprint.PrettyPrinter(indent=2)
    #pp.pprint(terms)
    output = "\n".join("{}\t{}".format(k, v) for k, v in terms.items())
    print output
    f = open("output.dict", "w")
    f.write(str(output))
    f.close()
