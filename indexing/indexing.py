#import pprint
import json

terms = {}
amount = {}


def indexing(dictList):
    finalOutput = ""
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

    for word in terms:
        amount[word] = 0
        for docid in terms[word]:
            amount[word] = amount[word]+1

    for word in sorted(terms):
        testOutput = word+","+str(amount[word])+":<"
        for docid in sorted(terms[word]):
            testOutput = testOutput+"doc"+str(int(docid)+1)+","
            testOutput = testOutput+str(len(terms[word][docid]))+":<"+str(
                terms[word][docid]).replace("[", "").replace("]", "")+">;"
        testOutput = testOutput+">;"
        finalOutput = finalOutput + testOutput+"\n"
        # print testOutput

    #json_object = json.dumps(terms, indent=4)
    # print(json_object)
    output = "\n".join("{}\t{}".format(k, v) for k, v in terms.items())
    output.replace("{", "<")
    output.replace("}", ">")
   # print output
    f = open("output.dict", "w")
    f.write(finalOutput)
    f.close()
    
    return terms,amount,doc_i
