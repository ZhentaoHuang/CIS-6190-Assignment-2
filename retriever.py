"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-2)
This file is used to Perform the Online Processing task. Type -h for help.
"""

import argparse
import readline





def read_files(dictionary_file, postings_file, docids_file):

    # Construct keyword list
    dictionary = []
    lines = dictionary_file.readlines()  # Read the dictionary file
    count = 0
    for line in lines:
        stem, df = line[:-1].split(" ")
        dictionary.append((stem, count))  # Convert the document frequency to offset
        count = count + int(df)  # Adjust the offset for next stem
    
    # Construct posting list
    postings = []
    lines = postings_file.readlines()
    for line in lines:
        did, tf = line[:-1].split(" ")
        postings.append((int(did), int(tf)))
    
    # Construct docid lsit
    docids = []
    lines = docids_file.readlines()
    for line in lines:
        words = line[:-1].split(" ")
        docid = words[0]
        start_line_number = words[-1]
        title = " ".join(words[1:-1])
        docids.append((docid, title, start_line_number))
    
    
    return dictionary, postings, docids

def online_process(dictionary, postings, docids):

    print("The database is loded.")
    query = " "
    while(query not in ["quit", "q"]):
        query = input("Please enter for quering (\"quit\" or \"q\" to quit): ")
        print("You entered: " + query)


    
def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    #parser.add_argument("-i", "--Input", default="samples.processed", help = "The input file (default: samples.splitted)")
    parser.add_argument("-d", "--Dictionary", default="dictionary.txt", help = "The input dictionary file (default: dictionary.txt)")
    parser.add_argument("-p", "--Postings", default="postings.txt", help = "The input postings file (default: postings.txt)")
    parser.add_argument("-s", "--Docids", default="docids.txt", help = "The input docids file (default: docids.txt)")

    
    # Read arguments from command line
    args = parser.parse_args()
    
    #print("Input: %s" % args.Input)
    print("Output as: % s" % args.Dictionary)
    print("Output as: % s" % args.Postings)
    print("Output as: % s" % args.Docids)

    return args

def main(args):

    #input = open(args.Input, 'r')
    dictionary_file = open(args.Dictionary, 'r')
    postings_file = open(args.Postings, 'r')
    docids_file = open(args.Docids, 'r')

    
    dictionary, postings, docids = read_files(dictionary_file, postings_file, docids_file)
    online_process(dictionary, postings, docids)
    
    
    dictionary_file.close()
    postings_file.close()
    docids_file.close()

if __name__ == "__main__":

    args = arg_parse()
    main(args)

