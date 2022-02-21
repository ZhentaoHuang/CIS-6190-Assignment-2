"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-2)
This file is used to Perform the preprocessing task. Type -h for help.
"""
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import argparse
import re
import string





def preproc(input, output):
    """This function is used for preprocessing. It performs 4 tasks: 
    1. Remove the PUNCTUATION, DELIMITERS and NUMBER
    2. Remove the stopwords
    3. Lowercase the words
    4. Convert the words into their stem

    Args:
        infile (file): input file
        outfile (file): output file
    """



    lines = input.readlines()
    ps = PorterStemmer()
    numbers = re.compile(r"[+|-]?\d+(\.\d+)?") # Integers and real numbers, with possible positive and negative signs

    count = 0
    for line in lines:

        value_list = []
        words = line[:-1].split(" ")
        # Check for the label
        if words[0] in ["$DOC", "$TITLE", "$TEXT"]:
            value_list.append(line[:-1])
            
        else:
            
            for word in words:
                match = numbers.match(word)  # Remove all the numbers
                if match is None and word not in string.punctuation:    # Remove the punctuation
                    if word not in stopwords.words("english"):  # Remove the stopwords

                        value_list.append(ps.stem(word.lower()))    # Lowercase and Stemming

        output.write(' '.join(value_list) + '\n')	# Write the ouput to the file based on value_list
        if (count % 5000 == 0):
            print(str(count) + " Line Processed")
        count = count + 1


    
def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-i", "--Input", default="documents_small.tokenized", help = "The input file (default: documents_small.tokenized)")
    parser.add_argument("-o", "--Output", default="documents_small.processed", help = "The output file (default: documents_small.processed)")
    
    # Read arguments from command line
    args = parser.parse_args()
    
    print("Input: %s" % args.Input)
    print("Output as: % s" % args.Output)

    return args

def main(args):

    input = open(args.Input, 'r')
    output = open(args.Output, 'w')
    
    preproc(input, output)

    input.close()
    output.close()

if __name__ == "__main__":

    args = arg_parse()
    main(args)

