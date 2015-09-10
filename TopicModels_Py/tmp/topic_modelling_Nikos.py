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


	wordRE = re.compile(r'[A-Za-z][A-Za-z]+')

	
	fids =  os.listdir(corpus_path)	
	
	stops = stopwords.words('english')

	# corpus iterator
	# produces docs.csv
	class MyCorpus(object):
		def __iter__(self):
			
			outfile = codecs.open(odir+'/docs.csv','w','utf-8')
			outfile.write('id,text,title\n')

			# for each file id
			for f in fids:
			
				if f == '.DS_Store':continue
				
				#detecting encoding
				infile = open(corpus_path+'/'+f,'r')
				data = infile.read()
				infile.close()
				enc = chardet.detect(data)['encoding']			
				
				# read text		
				infile = codecs.open(corpus_path+'/'+f,encoding=enc,mode='r')
				data = smart_unicode(infile.read())
				infile.close()
				
				
				data = data.replace('\"','\'')
				data = data.replace('\n','<br>')
				
				# find the title of the document (ad hoc for NYT :)) 
				title = "No title found"
				titleRE = re.search(r"<br><br>(.*?)<br><br>(.*?)<br><br>(.*)",data)
				if titleRE: 
					title = titleRE.group(1)
					data = titleRE.group(3)

				# write csv
				outfile.write(smart_unicode(f+',\"'+force_text(data)+'\",\"'+force_text(title)+'\"\n'))

				# assume there's one document per file, tokens separated by regex
				data = wordRE.findall(data.lower())
				# removing stop words and words of length<3
				yield [x for x in data if x not in stops and len(x)>2]
			outfile.close()
	
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
	outfile = open(odir+'/doc_ids','w')
	doc_text = '\n'.join(fids[1:])
	outfile.write(doc_text)
	outfile.close()	

	# Creating a gensim corpus (see gensim documentation)
	corpus = [dictionary.doc2bow(doc) for doc in corpus]

	# lda training (see gensim documentation for online LDA, here we use serial LDA)
	lda = gensim.models.ldamulticore.LdaMulticore(corpus, id2word=dictionary, num_topics=num_topics, passes=5)
	lda.save(odir+'/LDAmodel')	
	#lda = gensim.models.ldamulticore.LdaMulticore.load(odir+'/LDAmodel')
	
	# document topic matrix
	logger.info('Writing document topic matrix')
	docTopic = lda[corpus] #transforming documents to probability distributions over topics
	outfile_docTopic_csv = open(odir+'/docTopic.csv','w')
	outfile_docTopic_txt = open(odir+'/docTopic','w')
	outfile_docTopic_csv.write('\"doc_id\",\"topic_id\",\"probability\"\n')
	count=0 # 1 if you run on Mac, 0 otherwirse (handling .DStore of MacOS)
	for doc in docTopic:
		fid = fids[count]
		count+=1
		for tup in doc:
			outfile_docTopic_csv.write(fid+','+str(tup[0])+','+str(tup[1])+'\n')
			outfile_docTopic_txt.write(fid+' '+str(tup[0])+' '+str(tup[1])+'\n')
	outfile_docTopic_csv.close()
	outfile_docTopic_txt.close()

	
	# topic word matrix
	logger.info('Writing word topic matrix')
	wordTopic = lda.show_topics(num_topics,-1,formatted=False)
	outfile_WordTopic_csv = open(odir+'/wordTopic.csv','w')
	outfile_WordTopic_txt = open(odir+'/wordTopic','w')
	outfile_WordTopic_csv.write('\"word\",\"topic_id\",\"probability\"\n')
	for i in range(len(wordTopic)):
		for j in range(len(wordTopic[i])):
			if wordTopic[i][j][0]==0.0:continue
			outfile_WordTopic_csv.write('\"'+wordTopic[i][j][1]+'\",'+str(i)+','+str(wordTopic[i][j][0])+'\n')
			outfile_WordTopic_txt.write(wordTopic[i][j][1]+' '+str(i)+' '+str(wordTopic[i][j][0])+'\n')
	outfile_WordTopic_csv.close()
	outfile_WordTopic_txt.close()


	# document similarities
	sims = MatrixSimilarity(lda[corpus]) # get the pairwise similarities (cosine of the document vectors (probability distributions over topics))
	sims.num_best = 20 #number of similar documents threshold
	outfile_DocSim_csv = open(odir+'/DocSim.csv','w')
	outfile_DocSim_csv.write('\"doc1_id\",\"doc2_id\",\"similarity\"\n')
	count=0 # 1 if you run on Mac, 0 otherwirse (handling .DStore of MacOS)
	for doc in lda[corpus]:
		fid1 = fids[count] # fids[count+1] when on Mac, fids[count] otherwise 
		count+=1
		
		doc_sim = sims[doc]

		for tup in doc_sim:
			fid2 = fids[tup[0]]
			if fid2 != fid1 and str(tup[1])>=0.1: #store only doc pairs with similarity > 0.1
				outfile_DocSim_csv.write(fid1+','+fid2+','+str(tup[1])+'\n')
	outfile_DocSim_csv.close()
	


