"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-1)
This file is used to Perform the preprocessing task. Type -h for help.
"""
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from tokenization import scan, t_error
import argparse





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

    count = 0
    for line in lines:
        value_list = []
        
        if count == 10:
            break

        token_list = scan(line[:-1]) # The scan function is taken from Assignment 1, it returns the token list of the line.
        for tok in token_list:

            if tok.type != "PUNCTUATION" and tok.type != "DELIMITERS" and tok.type != "NUMBER": # Remove the PUNCTUATION, DELIMITERS and NUMBER
                if not tok.value in stopwords.words():  # Remove the stopwords. Inspired by the sample program.
                    if tok.type == "LABEL":
                        value_list.append(tok.value)
                    else:
                        value_list.append(ps.stem(tok.value.lower()))   # First lowercase the words then convert them into their stems. Inspired by the sample program.

        output.write(' '.join(value_list) + '\n')	# Write the ouput to the file based on value_list
        count = count + 1

    
def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-i", "--Input", default="samples.splitted", help = "The input file (default: samples.splitted)")
    parser.add_argument("-o", "--Output", default="samples.processed", help = "The output file (default: samples.processed)")
    
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

