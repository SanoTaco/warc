import json
#import time

def indexing(dictList):
    #tStart = time.time()
    terms = {}
    amount = {} 
    finalOutput="{\n"
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
        #print str(doc_i)+"dictList done."
    for word in terms:
        amount[word] = 0
        for docid in terms[word]:
            amount[word] = amount[word]+1
        #print str(word)+"vv done."
    for word in sorted(terms):
        testOutput ="'" +word+"':{'df':"+str(amount[word])+","
        for docid in sorted(terms[word]):
            testOutput = testOutput+"'doc"+str(int(docid)+1)+"':{'tf':"+str(len(terms[word][docid]))+","
            testOutput = testOutput+"'pos':"+str(terms[word][docid])+"},"
        testOutput = testOutput+"},"
        testOutput = list(testOutput)
        testOutput[len(testOutput)-3]=''
        #print str(word)+" has been done."
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

    #tEnd = time.time()
    #print ("Indexing cost %f sec" % (tEnd - tStart))
