"""Author: Zhentao Huang (Github link for this assignment: https://github.com/ZhentaoHuang/CIS-6190-Assignment-2)
This file is used to Perform the Offline Processing task. Type -h for help.
"""

import argparse


class document:
    """ A class store all the information of a single document (taken from assignment 1)
    """

    did = 0        # Document ID
    docid = ""      # Relative Document Number
    content = ""    # The whole content of the document
    index = 0       # Indicates the start of a document in the text
    title = ""      # The title of the document

    def __init__(self, docid, index, did):
        self.docid = docid
        self.index = index
        self.did = did

    def postproc(self):
        """This function is used to get rid of the labels and "\n" in the content for further analysis
        """
        count = 0
        processed_content = []
        for line in self.content:

            words = line[:-1].split(" ")
            # Check for the label
            if words[0] not in ["$DOC", "$TITLE", "$TEXT"]:
                processed_content.append(line[:-1])
            elif words[0] == "$TITLE":
                self.title = self.content[count + 1][:-1]
            count = count + 1
        self.content = processed_content

       
def read_documents(input):
    """This function is used to initialize the document objects and call the post-processing function for further calculation

    Args:
        input (file): input file

    Returns:
        docs: a list of document objects
    """

    lines = input.readlines()
    docs = []
    count = 0
   
    # Read the "$DOC" and set the index of the document object
    for line in lines:
        if line[:4] == "$DOC":
            docid = line[:-1].split(" ")[-1]
            doc = document(docid, count, len(docs))
            docs.append(doc)
            
        count = count + 1

    # Set the content of each document based on current index and next one's index
    for i in range(len(docs)):
        if i == len(docs) - 1:  # If it is the last one, set it to the end of the file
            docs[i].content = lines[docs[i].index:]
        else:
            docs[i].content = lines[docs[i].index:docs[i+1].index]
        
    # Post-processing for documents
    for doc in docs:
        doc.postproc()

    return docs


def offline_process(input, dictionary, postings, docids):
    """This function is used to perform the offline processing task. It takes preprocessed file as input and output three files:
    1. dictionary.txt (contains all stems along with their document frequencies)
    2. postings.txt (the concatenation of all posting entries associated with the related stems ordered by the increasing values of the stems)
    3. docids.txt (the set of docids along with their titles and starting line numbers in the input file)
    Args:
        input (file): input file
        dictionary (file): dictionary.txt
        postings (file): postings.txt
        docids (file): docids.txt
    """

    documents = read_documents(input)
    index = {}
    for doc in documents:
        for line in doc.content:
            words = line.split(" ")
            for word in words:
                # if the stem is not on the dictionary:
                if word not in index:
                    # add the stem to the dictionary and associate it with a list of one posting entry that has did set to
                    # the current document number and tf to 1
                    index[word] = [[doc.did,1]]
                # else if the stem is on the dictionary: get the associated list for the stem
                else:
                    # if the last entry’s did equals the current document number:
                    if index[word][-1][0] == doc.did:
                        # increase its tf by 1
                        index[word][-1][1] = index[word][-1][1] + 1
                    else:
                        index[word].append([doc.did,1])
    

    items = index.items()
    sorted_items = sorted(items)    # Sort the stems in increasing value

    # Output three files
    for item in sorted_items:
        # <stem1> <document-frequency1>
        dictionary.write(item[0] + " " + str(len(item[1])) + "\n")

        for posting in item[1]:
            # <did1> <tf1>
            postings.write(str(posting[0]) + " " + str(posting[1]) + "\n")
       
    for doc in documents:
        # <docid1> <title1> <start-line-number1>
        docids.write(doc.docid + " " + doc.title + " " + str(doc.index) + "\n")

    return



    
def arg_parse():
    """This function is used for command line argument parsing. It utilizes the argparse library. It provides the user with file choice at runtime.

    Returns:
        args: command line arguments
    """

    # Initialize parser
    parser = argparse.ArgumentParser()
    
    # Adding optional argument
    parser.add_argument("-i", "--Input", default="samples.processed", help = "The input file (default: samples.splitted)")
    parser.add_argument("-d", "--Dictionary", default="dictionary.txt", help = "The output file (default: dictionary.txt)")
    parser.add_argument("-p", "--Postings", default="postings.txt", help = "The output file (default: postings.txt)")
    parser.add_argument("-s", "--Docids", default="docids.txt", help = "The output file (default: docids.txt)")

    
    # Read arguments from command line
    args = parser.parse_args()
    
    print("Input: %s" % args.Input)
    print("Output as: % s" % args.Dictionary)
    print("Output as: % s" % args.Postings)
    print("Output as: % s" % args.Docids)

    return args

def main(args):

    input = open(args.Input, 'r')
    dictionary = open(args.Dictionary, 'w')
    postings = open(args.Postings, 'w')
    docids = open(args.Docids, 'w')
    
    offline_process(input, dictionary, postings, docids)

    input.close()
    dictionary.close()
    postings.close()
    docids.close()

if __name__ == "__main__":

    args = arg_parse()
    main(args)

