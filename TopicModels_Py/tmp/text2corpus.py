import gensim
import os, glob
import numpy

##################################################
# -- dummy text
articles = ["Human machine interface for lab abc computer applications",
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
        articles.append(filecontent.read())

##################################################
# -- real text from Juicer
articles = numpy.load("articleList_100.npy")


# -- change \n into space
articles = [a.replace('\n', ' ') for a in articles]


# -- remove punctiation - QUICK & DIRTY
## ACHTUNG: this removes all punctuation, apostrophes and also
## accented characters (i.e. ü, ñ, é) - refine this step !!!
import regex
articles = [regex.sub(ur"\p{P}+", "", a) for a in articles]


# -- to lower case
articles = [a.lower() for a in articles]


# -- remove common words 
import nltk
# nltk.download() # identifier: stopwords
from nltk.corpus import stopwords
s=set(stopwords.words('english'))

def removeStopWords(article):
    resultwords  = [word for word in article.split() if word not in s]
    result = ' '.join(resultwords)
    return result
articles = [removeStopWords(a) for a in articles]


# -- stemming


# -- handling numbers


# -- tokenise
articles = [a.split() for a in articles]


# remove words that appear only x times
# TODO: plot frequency distribution of words overall
from collections import defaultdict
frequency = defaultdict(int)
for text in articles:
    for token in text:
        frequency[token] += 1

    articles = [[token for token in text if frequency[token] > 1]
         for text in articles]


# transform list into occurrance matrix
dictionary = gensim.corpora.Dictionary(articles)
print(dictionary)
print(dictionary.token2id)

dictionary.save('dictionary_0824.dict') # store the dictionary, for future reference

corpus = [dictionary.doc2bow(a) for a in articles]
print(corpus)


# instead of keeping all of this in memory, write the articles in a file, one article
# per line, which can easily be read into a corpus

class MyCorpus(object):
     def __iter__(self):
         for line in open('mycorpus.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())

