import sys
import os
import shutil
import time
from process.process import preProcessing
from indexing.indexing import indexing
from query.query import query
from process.process import parsing
from query.query import query_bs


def create():
    tStart = time.time()
    # time.sleep(2)
    input_file = sys.argv[1]
    print ("Start ......")
    print ("Parsing HTML ......")
    print ("Dumping ......")
    index = preProcessing(input_file)
    dictList = parsing(index)
    indexing(dictList)
    print ("Finish !!!")
    tEnd = time.time()
    print ("It cost %f sec" % (tEnd - tStart))


if __name__ == "__main__":
    doc_id = 0
    if "-c" in sys.argv:
        create()
    elif "-s" in sys.argv:
        if not os.path.isfile("output.dict") or not os.path.isfile("page.total"):
            print ("Error: Can not dict file ! ")
            exit(1)
        else:
            query()
    elif "-bs" in sys.argv:
        if not os.path.isfile("output.dict") or not os.path.isfile("page.total"):
            print ("Error: Can not dict file ! ")
            exit(1)
        else:
            query_bs()
    else:
        print ("Error: Please use -c or -s to run ! ")
        exit(1)
