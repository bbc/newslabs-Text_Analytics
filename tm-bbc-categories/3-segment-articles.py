# -*- coding: utf-8 -*-
import gensim
import sys,os
from nltk.corpus import stopwords
import logging, types, re
from django.utils.encoding import smart_str, smart_unicode, smart_text, force_text
import codecs
import chardet
import re
from gensim.similarities import *

# Script for training an LDA model
# Input:
# 	corpus_path: path to the collection of documents
#	num_topics: number of LDA topics	 
#
# Output:
#	wordTopic: topic-word matrix
#	docTopic:  doc-topic matrix
#	vocab:	vocabulary
#	docDoc: document similarity

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def train(corpus_path,odir,num_topics=10):

	# create output folder
	if not os.path.exists(odir):
    		os.makedirs(odir)


    # article IDs
	aIDs =  []

	# article section
	aSecs = []

	wordRE = re.compile(r'[A-Za-z][A-Za-z]+')

	stops = stopwords.words('english')

	# corpus iterator
	# produces docs.csv
	class MyCorpus(object):
		def __iter__(self):
			
			#detecting encoding
			infile = open(corpus_path,'r')
			data = infile.read()
			infile.close()
			enc = chardet.detect(data)['encoding']			
				
			# read text		
			infile = codecs.open(corpus_path,encoding=enc,mode='r')
	
			# for each news article in the file
			with infile as f:	
				for line in f:
					
					linevec = re.split(r'\t+', line)
					
					aID = linevec[1]
					aIDs.append(aID)

					data  = linevec[3]
					data = data.replace('\"','\'')

					aSec = linevec[4].strip()
					aSecs.append(aSec)

					# assume there's one document per file, tokens separated by regex
					data = wordRE.findall(data.lower())
					# removing stop words and words of length<3
					yield [x for x in data if x not in stops and len(x)>2]
				
			infile.close()

	#load corpus
	corpus = MyCorpus()
		 
	# create LDA vocabulary (see gensim documentation)
	dictionary = gensim.corpora.Dictionary(doc for doc in corpus)
	# keep top 1000 words with doc freq > 10, appearing in less than 30% of the documents (see gensim dictionary)
	dictionary.filter_extremes(no_below=10,no_above=0.3,keep_n=700)
	dictionary.save(odir+'/DictLDA')
	#dictionary = gensim.corpora.Dictionary.load(odir+'/DictLDA')
	outfile = open(odir+'/vocab','w')
	#store dictionary as list of words (one at each line)
	dic_text = '\n'.join(dictionary.values())
	outfile.write(dic_text)
	outfile.close()	
	
	# storing topics 
	outfile = open(odir+'/topics','w')
	topic_text = '\n'.join([str(t) for t in range(num_topics)])
	outfile.write(topic_text)
	outfile.close()	
	
	# storing document ids
	#outfile = open(odir+'/doc_ids','w')
	#doc_text = '\n'.join(fids[1:])
	#outfile.write(doc_text)
	#outfile.close()	

	# Creating a gensim corpus (see gensim documentation)
	corpus = [dictionary.doc2bow(doc) for doc in corpus]

	# lda training (see gensim documentation for online LDA, here we use serial LDA)
	lda = gensim.models.ldamulticore.LdaMulticore(corpus, id2word=dictionary, num_topics=num_topics, passes=5)
	lda.save(odir+'/LDAmodel')	
	#lda = gensim.models.ldamulticore.LdaMulticore.load(odir+'/LDAmodel')
	
	# -------------------------------------------
	# document-topic matrix
	# -------------------------------------------
	logger.info('Writing document topic matrix')
	docTopic = lda[corpus] #transforming documents to probability distributions over topics
	outfile_docTopic_csv = open(odir+'/docTopic.csv','w')
	outfile_docTopic_csv.write('\"section\",\"doc_id\",\"topic_id\",\"probability\"\n')
	count=0 # 1 if you run on Mac, 0 otherwise (handling .DStore of MacOS)
	for doc in docTopic:
		aID = aIDs[count]
		aSec = aSecs[count]
		count+=1
		for tup in doc:
			outfile_docTopic_csv.write(aSec +','+ aID+','+str(tup[0])+','+str(tup[1])+'\n')
	outfile_docTopic_csv.close()

	
	# -------------------------------------------
	# topic-word matrix
	# -------------------------------------------
	logger.info('Writing word topic matrix')
	wordTopic = lda.show_topics(num_topics,10,formatted=False)
	print wordTopic

	outfile_WordTopic_csv = open(odir+'/wordTopic.csv','w')
	outfile_WordTopic_csv.write('\"topic_id\",\"word\",\"probability\"\n')
	
	outfile_WordTopic_string = 	open(odir+'/wordTopic.string','w')

	for i in range(len(wordTopic)):
		
		outfile_WordTopic_string.write(str(wordTopic[i][0])+"\t")

		for j in range(len(wordTopic[i][1])):

			outfile_WordTopic_csv.write(str(wordTopic[i][0])+','+'\"'+str(wordTopic[i][1][j][0])+'\",'+str(wordTopic[i][1][j][1])+'\n')
			outfile_WordTopic_string.write(str(wordTopic[i][1][j][0])+',')
	
	
		outfile_WordTopic_string.write("\n")

	outfile_WordTopic_csv.close()
	outfile_WordTopic_string.close()

# -------------------------------------------
# go
# -------------------------------------------

print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

# argv[0] = function
# argv[1] = dataset
# argv[2] = output folder
# argv[3] = number of topics

train(sys.argv[1], sys.argv[2], int(sys.argv[3]))

	
