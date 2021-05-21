# CS172 - Assignment 1 (Tokenization)

## Team member 1 - Shray Grover
## Team member 2 - Cristina Lawson

###### Provide a short explanation of your design

We implemented a way to tokenize words by first removing punctuation and lowercasing the words, and then stemming the words using an external library.

After this, we implemented an index by making multiple dictionary data structures, listed below:

key -> value
1. term -> termId
2. docNo -> docID
3. term -> docno, docFreq, positions

We then used these data structures in order to retrieve the required information when the user passes in their information in the command line.

###### Language used, how to run your code, if you attempted the extra credit (stemming), etc. 

Language used: Python

How to run code: python3 read_index.py *input*

Extra Credit: stemming
