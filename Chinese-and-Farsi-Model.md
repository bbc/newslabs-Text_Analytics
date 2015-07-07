# Training of the Mango models for the Chinese and Farsi languages

This document describes the process of training the models for the Chinese and Farsi languages. The resulting models have been uploaded to the [S3 Bucket](https://s3.amazonws.com/newslabs-mango)

## The model for the Farsi language

### An index generated from the DBpedia labels

- Download the labels in the Farsi language from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/fa/labels_fa.nt.bz2
- Download the redirects_transitive file from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/fa/redirects_transitive_fa.nt.bz2
- Unzip those two files
- Run `dbpedia-resolve-redirects --input-labels ./labels_fa.nt --transitive-redirects ./redirects_transitive_fa.nt --output-labels labels.fa`
- Download and unzip the instance types file from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/en/instance_types_en.nt.bz2
- Run `mango-create-index --input-labels labels.fa --input-types instance_types_en.nt --output-index dbpedia_index.db`

### A Word2Vec model generated from Wikipedia

- Download Wikipedia pages from http://dumps.wikimedia.org/fawiki/latest/fawiki-latest-pages-articles.xml.bz2
- Use the Mango Java tool to create the training set, i.e. run the following command:

```
    $JAVA bbc.rd.mango.CreateTrainingSet \
    --wikipedia-xml-dump fawiki-latest-pages-articles.xml.bz2 \
    --output-file training.txt \
    --transitive-redirects redirects_transitive_fa.nt.bz2
```

- Train the word2vec model by executing the following command:

```
    word2vec -train training.txt -output model.bin \
    -cbow 0 -size 300 -window 10 -negative 0 \
    -hs 1 -sample 1e-3 -threads 24 -binary 1 \
    -save-vocab vocab.txt
```

- Finally, transform the word2vec model into Mango model

```
    mango-word2vec-model-to-mango \
    --word2vec-model model.bin \
    --word2vec-vocab vocab.txt \
    --directory model
```


## The model for the Chinese language

### An index generated from the DBpedia labels

- Download the labels in the Chinese language from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/zh/labels_zh.nt.bz2
- Download the redirects_transitive file from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/zh/redirects_transitive_zh.nt.bz2
- Unzip those two files
- Run `dbpedia-resolve-redirects --input-labels ./labels_zh.nt --transitive-redirects ./redirects_transitive_zh.nt --output-labels labels.zh`
- Download and unzip the instance types file from http://data.dws.informatik.uni-mannheim.de/dbpedia/2014/en/instance_types_en.nt.bz2
- Run `mango-create-index --input-labels labels.zh --input-types instance_types_en.nt --output-index dbpedia_index.db`

### A Word2Vec model generated from Wikipedia

- Download Wikipedia pages from http://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2
- Use the Mango Java tool to create the training set, i.e. run the following command:

```
    $JAVA bbc.rd.mango.CreateTrainingSet \
    --wikipedia-xml-dump zhwiki-latest-pages-articles.xml.bz2 \
    --output-file training.txt \
    --transitive-redirects redirects_transitive_zh.nt.bz2
```

- Train the word2vec model by executing the following command:

```
    word2vec -train training.txt -output model.bin \
    -cbow 0 -size 300 -window 10 -negative 0 \
    -hs 1 -sample 1e-3 -threads 24 -binary 1 \
    -save-vocab vocab.txt
```

- Finally, transform the word2vec model into Mango model

```
    mango-word2vec-model-to-mango \
    --word2vec-model model.bin \
    --word2vec-vocab vocab.txt \
    --directory model
```

### Changes to the Mango source codes

As the Chinese language needs to do the segmentation before Named Entity Recognition (NER), a Python library called [Jieba](https://github.com/fxsjy/jieba) has been integrated into the Mango server. Relevant changes have been submitted to a separate branch on [GitLab](http://gitlab.prototype0.net/yves.raimond/abcip_mango/tree/chinese).
