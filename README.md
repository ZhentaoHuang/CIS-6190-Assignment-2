# CIS-6190-Assignment-2
UofG grad course CIS-6190 Assignment 2


Test Environment: Python 3.7.2 linux.socs.uoguelph.ca



* # 1. Pre-processing
  * ## Usage
  ```python preprocessor.py --Input YourInputFile --Output YourOutputFile```

  The input is set to documents_small.tokenized, and the output is set to documents_small.processes in default. The program should print out the progress every 5,000 lines of documents.

  * ## Objectives
  The goal is to perform 4 processing tasks:
  1. Normalization: convert all token values into lower cases.
  2. Further Filtering: remove numbers and punctuation marks.
  3. Stop Word Removal: remove all stop words in English (such as "the", "a", "of").
  4. Stemming: convert the remaining words to their stems.
  
  * ## Test Plan
  The test cases are added at the top of documents_small.tokenized file. Such as "ComPuting" or "cOMPuter". Please check the file for full details.

* # 2. Offline Processing
  * ## Usage
  ```python indexer.py --Input YourInputFile --Dictionary YourOutputDictionaryFile --Postings YourOutputPostingsFile --Docids YourOutputDocidsFile```

  The input is set to documents_small.preprocessed, and the output is set to dictionary.txt, postings.txt, docids.txt in default.

  * ## Objectives
  The goal is to take the preprocessed file as input and produce an inverted index with three outputfiles: dictionary.txt, postings.txt and docids.txt.
  1. dictionary.txt: \<stem\> \<document-frequency\>
  2. postings.txt: \<did\> \<tf\>
  3. docids.txt \<docid\> \<title\> \<start-line-number\>
  
  
* # 3. Online Processing
  * ## Usage
  ```python retriever.py --Dictionary YourInputDictionaryFile --Postings YourInputPostingsFile --Docids YourInputDocidsFile```

  The input is set to dictionary.txt, postings.txt, docids.txt in default.

  * ## Objectives
  The goal of this program is to load the inverted files from the offline processing into memory and then ask for user's query iteratively. Then search for the top-10 relative documents based on tf.idf and inner products.

