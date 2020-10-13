import sys
from process.process import preProcessing

def main():
    input_file = sys.argv[1]
    print("Start ......")
    preProcessing(input_file)
    print("Parsing HTML ......")
    print("finish")

if __name__ == "__main__":
    main()