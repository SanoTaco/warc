import sys
import os
import shutil
from process.process import preProcessing
from indexing.indexing import indexing

path = 'output_htmls'
if not os.path.exists(path):
    os.makedirs(path)


def main():
    input_file = sys.argv[1]
    print("Start ......")
    print("Parsing HTML ......")
    print("Dumping ......")
    dictList = preProcessing(input_file)
    indexing(dictList)
    print("Finish !!!")
    shutil.rmtree(path)


if __name__ == "__main__":
    main()
