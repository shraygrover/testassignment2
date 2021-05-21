# This file should contain code to receive either a document-id or word or both and output the required metrics. See the assignment description for more detail.

import parsing
import sys

termIndex, termInfo, docIndex = parsing.Tokens()

if (len(sys.argv) == 3):
    inputType1 = sys.argv[1]
    input1 = sys.argv[2]

    if (inputType1 == '--term'):
        print('Listing for term: ', input1)
        print('TERMID: ', termIndex.get(input1))
        print('Number of documents containing term: ', termInfo.get(input1).get('numDocs'))
        print('Term frequency in corpus: ', termInfo.get(input1).get('numOccur'))

    if (inputType1 == '--doc'):
        print('Listing for document: ', input1)
        info = docIndex.get(input1).get('docID')
        print('DOCID: ', info)
        print('Distinct terms: ', docIndex.get(input1).get('distinctTerms'))
        print('Total terms: ', docIndex.get(input1).get('totalTerms'))

if (len(sys.argv) == 5):
    inputType1 = sys.argv[1]
    inputType2 = sys.argv[3]

    if (inputType1 == '--term'):
        term = sys.argv[2]
        print('Inverted term for term: ', term)
        info = termIndex.get(term)
        print('TERMID: ', info)

    if (inputType1 == '--doc'):
        doc = sys.argv[2]
        print('In document: ', doc)
        info = docIndex.get(doc).get('docID')
        print('DOCID: ', info)

    if (inputType2 == '--term'):
        term = sys.argv[4]
        print('Inverted term for term: ', term)
        info = termIndex.get(term)
        print('TERMID: ', info)

    if (inputType2 == '--doc'):
        doc = sys.argv[4]
        print('In document: ', doc)
        info = docIndex.get(doc).get('docID')
        print('DOCID: ', info)

    print('Term frequency in document: ', termInfo.get(term).get('postingList').get(doc))
    print('Positions: ', termInfo.get(term).get('postingList').get(doc).get('positions'))