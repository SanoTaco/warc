import sys
import os
import shutil
from process.process import preProcessing
from indexing.indexing import indexing
from query.query import query



def create():
    path = 'output_htmls'
    if not os.path.exists(path):
        os.makedirs(path)
    input_file = sys.argv[1]
    print "Start ......"
    print "Parsing HTML ......"
    print "Dumping ......" 
    dictList = preProcessing(input_file)
    indexing(dictList)
    print "Finish !!!"
    shutil.rmtree(path)


if __name__ == "__main__":
    doc_id=0
    if "-c" in sys.argv:
        create()
    elif "-s" in sys.argv:
        if not os.path.isfile("output.dict") or not os.path.isfile("page.total"):
            print "Error: Can not dict file ! "
            exit(1)
        else:
            query()
    else:
        print "Error: Please use -c or -s to run ! "
        exit(1)
