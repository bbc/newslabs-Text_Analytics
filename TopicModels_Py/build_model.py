#################################################
## Load dictionary, (re-)build model 
#################################################
import gensim
import os, glob
import numpy
import nltk
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

## ----- Load dictionary
load('newsDictionary')


## ----- Build the corpus matrix

class MyCorpus(object):
     def __iter__(self):
         for line in open('../articles/JuicerArticles_500.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())


corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
print(corpus_memory_friendly)

for vector in corpus_memory_friendly: # load one vector into memory at a time
    print(vector)


## ----- Transformation

gensim.corpora.MmCorpus.serialize('corpus.mm', corpus_memory_friendly)
corpus = gensim.corpora.MmCorpus('corpus.mm')
print(corpus)

tfidf = gensim.models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

lsi.print_topics(1) # print topic IDs and connected words

for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
   print(doc)
