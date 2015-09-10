#################################################
## Build news dictionary
#################################################
import gensim
import os, glob
import numpy
import nltk
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

## ----- Build the dictionary

# collect statistics about all tokens
dictionary = gensim.corpora.Dictionary(line.lower().split() for line in open('../articles/JuicerArticles_100.txt'))

# remove stop words and words that appear only once
# stoplist = set('for a of the and to in'.split())
# nltk.download() # identifier: stopwords
stoplist = set(nltk.corpus.stopwords.words('english'))

stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
            if stopword in dictionary.token2id]

once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 1]
dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
dictionary.compactify() # remove gaps in id sequence after words that were removed
# print(dictionary)
dictionary.save('newsDictionary')


## ----- Build the corpus matrix

class MyCorpus(object):
     def __iter__(self):
         for line in open('../articles/JuicerArticles_100.txt'):
             # assume there's one document per line, tokens separated by whitespace
             yield dictionary.doc2bow(line.lower().split())


corpus_memory_friendly = MyCorpus() # doesn't load the corpus into memory!
#print(corpus_memory_friendly)

#for vector in corpus_memory_friendly: # load one vector into memory at a time
#    print(vector)


## ----- Transformation

gensim.corpora.MmCorpus.serialize('corpus.mm', corpus_memory_friendly)
corpus = gensim.corpora.MmCorpus('corpus.mm')
#print(corpus)

tfidf = gensim.models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]
#for doc in corpus_tfidf:
#    print(doc)

lsi = gensim.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

lsi.print_topics(1) # print topic IDs and connected words

#for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
   #print(doc)
