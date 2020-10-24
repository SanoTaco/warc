import json

def indexing(dictList):
    terms = {}
    amount = {} 
    finalOutput="{\n"
    doc_i = 0
    for docid in dictList:
        for word in dictList[docid]:
            if word not in terms:
                terms[word] = {}
            if str(doc_i) not in terms[word]:
                terms[word][str(doc_i)] = {}
            terms[word][str(doc_i)] = [
                i for i, e in enumerate(dictList[docid]) if e == word]
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

    f = open("output.dict", "w")
    f.write(realfinal)
    f.close()

    hama = open("page.total", "w")
    hama.write(str(doc_i))
    hama.close()
