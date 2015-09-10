from gensim import corpora, models, similarities
import os, glob

##################################################

documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

path = 'articles'

# open articles and append the text as one string to documents arrar
for filename in glob.glob(os.path.join(path, '*.txt')):
    print(filename)

    with open (filename) as filecontent:
        documents.append(filecontent.read())


# remove punctiation
import string
stringIn = "string.with.punctuation!"
out = stringIn.translate(stringIn.maketrans("",""), string.punctuation)


# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
        for text in texts]
from pprint import pprint   # pretty-printer
pprint(texts)

