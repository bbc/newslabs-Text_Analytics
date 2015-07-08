# Training of the Labeled LDA Model

This document introduces the approach to training the LDA models for automating the tagging process.

## Labeled LDA (Supervised LDA)

### Training data

676 news articles tagged with 755 instances of [core:Things](http://www.bbc.co.uk/ontologies/coreconcepts#terms_Thing) have been gathered to form the initial training dataset. This dataset is serialised in the format of JSON and available [here](https://dl.dropboxusercontent.com/u/3457032/tagging_gold_standard.json)

### Model training

The Labeled LDA model is trained using the [JGibbLabeledLDA](https://github.com/myleott/JGibbLabeledLDA), which is a Java implementation of the Labeled LDA algorithm. The training set is created by taking the following steps

- The tags associated to the news stories are treated as labels. In order to facilitate the model training, a simple numeric index is created for the tags.
- The stop words and punctuations in content of the news stores are filtered out before doing the training.
- The parameters used to in the training are `-est -ntopics 10 -niters 1000 -nburnin 400 -samplinglag 200 -twords 30`


### Results

The labeled LDA model training results in: the word-topic distributions, the topic-document distributions, the topic assignments for words in training data and the most-likely words for each topic. A simple Web-based interface, i.e. [Mango Satsuma](http://sentinet-mango.abdn.ac.uk/satsuma), has been established to test the resulting LDA model.

## Unsupervised LDA

Since the training data got from the LDP may have some faults. For example, a news story about the animal 'cats' might be tagged with the west-end musical 'Cats' by mistake. Therefore, we are thinking about using the unsupervised LDA so that we could avoid putting the imperfect data into the training set. The idea is to compare the similarity between news articles by using a unsupervised LDA model, and then recommend some tags according to the up-to-date tagging results of those similar news articles.
