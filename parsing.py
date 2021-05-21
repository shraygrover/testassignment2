import re
import os
import zipfile
import time
import sys
from nltk.stem.lancaster import LancasterStemmer

def Tokens():
    lancaster = LancasterStemmer()

    # Regular expressions to extract data from the corpus
    doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
    docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
    text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)


    with zipfile.ZipFile("ap89_collection_small.zip", 'r') as zip_ref:
        zip_ref.extractall()

    # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
    for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
        allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]

    termInfo = dict()
    docIndex = dict()
    termIndex = dict()

    for file in allfiles:
        with open(file, 'r', encoding='ISO-8859-1') as f:
            filedata = f.read()
            result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents

            for document in result[0:]:
                # Retrieve contents of DOCNO tag
                docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                # Retrieve contents of TEXT tag
                text = "".join(re.findall(text_regex, document))\
                          .replace("<TEXT>", "").replace("</TEXT>", "")\
                          .replace("\n", " ")

                punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
                no_punct = ""
                for ele in text:
                  if ele not in punc:
                        no_punct = no_punct + ele
                no_punct = no_punct.lower()
                text = no_punct

                stopFile = open("stopwords.txt", "r")
                stopWords = stopFile.read()
                stopWords = stopWords.replace("\n", " ")

                textList = list(text.split(' '))
                stopList = list(stopWords.split(' '))

                textList = list(filter(None, textList))
                stopList = list(filter(None, stopList))

                # https://www.geeksforgeeks.org/python-difference-two-lists/
                tokens = [i for i in textList + stopList if i not in textList or i not in stopList]

                for i in range(len(tokens)):
                    tokens[i] = lancaster.stem(tokens[i])

                tokens = [i for i in tokens + stopList if i not in tokens or i not in stopList]

                docInfo = dict()
                docInfo['docID'] = hash(docno) % ((sys.maxsize + 1) * 2)
                docInfo['totalTerms'] = len(tokens)
                docInfo['distinctTerms'] = 0

                docIndex[docno] = docInfo

                position = 0
                distinct = 0

                for token in tokens:
                    hashToken = hash(token) % ((sys.maxsize + 1) * 2)

                    if token not in termIndex:
                        distinct = distinct + 1
                        termIndex[token] = hashToken
                        info = dict()
                        postList = dict()
                        docNumber = dict()
                        positions = list()

                        docNumber['freq'] = 0
                        docNumber['positions'] = positions

                        postList[docno] = docNumber

                        info['numOccur'] = 0
                        info['numDocs'] = 0
                        info['postingList'] = postList

                        termInfo[token] = info

                        termInfo[token]['numOccur'] = termInfo[token]['numOccur'] + 1
                        termInfo[token]['numDocs'] = termInfo[token]['numDocs'] + 1

                        posList = termInfo[token]['postingList'][docno]['positions']
                        posList.append(position)
                        termInfo[token]['postingList'][docno]['positions'] = posList
                        termInfo[token]['postingList'][docno]['freq'] = termInfo[token]['postingList'][docno]['freq'] + 1

                    elif token in termIndex:

                      if docno in termInfo[token]['postingList']:
                        posList = termInfo[token]['postingList'][docno]['positions']
                        posList.append(position)
                        termInfo[token]['postingList'][docno]['positions'] = posList
                        termInfo[token]['postingList'][docno]['freq'] = termInfo[token]['postingList'][docno]['freq'] + 1

                        termInfo[token]['numOccur'] = termInfo[token]['numOccur'] + 1

                      if docno not in termInfo[token]['postingList']:
                        docNumber = dict()
                        positions = list()
                        docNumber['freq'] = 0
                        docNumber['positions'] = positions

                        termInfo[token]['postingList'][docno] = docNumber

                        posList = termInfo[token]['postingList'][docno]['positions']
                        posList.append(position)
                        termInfo[token]['postingList'][docno]['positions'] = posList
                        termInfo[token]['postingList'][docno]['freq'] = termInfo[token]['postingList'][docno]['freq'] + 1

                        termInfo[token]['numOccur'] = termInfo[token]['numOccur'] + 1
                        termInfo[token]['numDocs'] = termInfo[token]['numDocs'] + 1

                    position = position + 1

                docIndex[docno]['distinctTerms'] = distinct

                # testing code
                #time.sleep(1)

                #exit()

    return termIndex, termInfo, docIndex