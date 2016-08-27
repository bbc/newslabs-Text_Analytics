# Part 2 - Converting URLs from Freebird to Text

install.packages("RCurl")
library(RCurl)

install.packages("XML")
library(XML)

install.packages("stringr")
library(stringr)

# Parse first URL from Freebird
doc_html <- htmlTreeParse(news_URL_1, useInternal = TRUE)

# Extract text and clean data
news_text <- unlist(xpathApply(doc_html, '//p', xmlValue))
news_text <- gsub('\\n', ' ', news_text)
news_text <- paste(news_text, collapse = ' ')
head(news_text)

# Extract numbers (e.g. from, say '60%')
numbers <- gregexpr("[0-9]+", news_text)
numbers_intext <- as.numeric(unique(unlist(regmatches(news_text, numbers))))

# Extract % from text
percent_notation <- gsub("[^%]"," ", news_text)

news_text <- paste(news_text, numbers_intext, percent_notation)


##### If looking to analyse your own news URL (e.g. this one from Quartz) - run the code through same as above
doc_html <- htmlTreeParse("http://qz.com/762729/poor-data-is-hurting-african-countries-ability-to-make-good-policy-decisions/", useInternal = TRUE)
