"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-1)
This file is used to split the title and text into sequence of strings. Type -h for help.
"""
from nltk import sent_tokenize
import argparse


def split(infile, outfile):
    """
    This function is used to conduct the sentence splitting for both title and body texts. 
    Inspired by the sample program.

    Args:
        infile (file): input file
        outfile (file): output file
    """
    lines = infile.readlines()
    section = []    #a temporary buffer used to store the section between labels
    for line in lines:
        if line[0] == '$':
            #if the first char in the line is "$", then the line is a label
            
            if len(section) == 0:
                #if therie is no lines in the "secton" then write the current label
                outfile.write(line)
                next
            else:
                #if there are contents in the "section", write the content first then write the label
                buffer = ' '.join(line[:-1] for line in section)
                sents = sent_tokenize(buffer)
                for sent in sents:
                    outfile.write(sent + '\n')
                section = []
                outfile.write(line)

        else:
            #if it is not label, add the line into "section"
            section.append(line)

    #Write what's left in the section when reach the end of the file       
    buffer = ' '.join(line[:-1] for line in section)
    sents = sent_tokenize(buffer)
    for sent in sents:
        outfile.write(sent + '\n')
    
def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-i", "--Input", default="samples.txt", help = "The input file (default: samples.txt)")
    parser.add_argument("-o", "--Output", default="samples.splitted", help = "The output file (default: samples.splitted)")
    
    # Read arguments from command line
    args = parser.parse_args()
    
    print("Input: %s" % args.Input)
    print("Output as: % s" % args.Output)

    return args

def main(args):

    input = open(args.Input, 'r')
    output = open(args.Output, 'w')
    
    split(input, output)

    input.close()
    output.close()

if __name__ == "__main__":

    args = arg_parse()
    main(args)

