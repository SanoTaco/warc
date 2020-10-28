import json


def indexing(dictList):
    terms = {}
    test = {}
    doc_i = 0
    for v in dictList:
        for word in v:
            if word not in terms:
                terms[word] = {}
            if str(doc_i) not in terms[word]:
                terms[word][str(doc_i)] = {}
            terms[word][str(doc_i)] = [
                i for i, e in enumerate(v) if e == word]
        doc_i = doc_i+1

    for word in sorted(terms):
        test[word] = {}
        test[word]["df"] = len(terms[word])
        for i in sorted(terms[word]):
            test[word][i] = {}
            test[word][i]["pos"] = terms[word][i]
            test[word][i]["tf"] = len(terms[word][i])

    json_object = json.dumps(test, indent=2, sort_keys=True)

    f = open("output.dict", "w")
    f.write(json_object)
    f.close()

    hama = open("page.total", "w")
    hama.write(str(doc_i))
    hama.close()
