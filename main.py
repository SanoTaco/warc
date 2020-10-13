import sys
import os
import shutil
from process.process import preProcessing

path = 'output_htmls'
pathDoc = 'document'
if not os.path.exists(path):
    os.makedirs(path)
elif not os.path.exists(pathDoc):
    os.makedirs(pathDoc)

def main():
    input_file = sys.argv[1]
    print("Start ......")
    preProcessing(input_file)
    print("Parsing HTML ......")
    print("finish")
    shutil.rmtree(path)

if __name__ == "__main__":
    main()