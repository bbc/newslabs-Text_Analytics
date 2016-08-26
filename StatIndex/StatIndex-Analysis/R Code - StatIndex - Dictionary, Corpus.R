# Part 3 - Corpus and dictionary-based approach

install.packages("tm")
library(tm)

install.packages("RWeka")
library(RWeka)

install.packages("reshape2")
library(reshape2)


# Read in dictionary of statistical terms and notation after downloading from Github
dictionary <- read.csv("statistical_data_dictionary_prelim.csv", header = TRUE, stringsAsFactors = FALSE)

# Read in corpus (example directory)
sf <- system.file("news_text", "txt", package = "tm")
ds <- DirSource("Projects/News_Text_Files")
news_content <- Corpus(ds)

# Data tidying and transformation for corpus
news_content_source <- VectorSource(news_text)
corpus <- Corpus(news_content_source)
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, stripWhitespace)
corpus <- tm_map(corpus, removeWords, stopwords("english"))


# Build term document matrix (tdm) for the news content containing all words in content
tdm <- TermDocumentMatrix(corpus)
inspect(tdm)
tdm <- as.matrix(tdm)


# Dataframe from term document matric containing frequency of statistical words in content
Terms <- as.data.frame(inspect(TermDocumentMatrix(corpus, list(dictionary = dictionary$content))))
Terms <- cbind(rownames(Terms), Terms)
rownames(Terms) <- NULL
colnames(Terms) <- c("content", "frequency")
Terms <- Terms[1:2]
print(Terms)

# Further analysis - Count the use of one word - 'data' in the news content
dictionary_2 <- c("data")
Term_Data <- inspect(TermDocumentMatrix(corpus, list(dictionary = dictionary_2)))
Term_Data <- cbind(rownames(Term_Data), Term_Data)
rownames(Term_Data) <- NULL
colnames(Term_Data) <- c("content", "frequency")
Term_Data <- Term_Data[1:2]
print(Term_Data)
