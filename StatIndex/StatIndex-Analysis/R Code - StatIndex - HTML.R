# Part 2 - Converting URLs from Freebird to Text

install.packages("RCurl")
library(RCurl)

install.packages("XML")
library(XML)

# Parse first URL from Freebird
doc_html <- htmlTreeParse(news_URL_1, useInternal = TRUE)

# Extract text and clean data
news_text <- unlist(xpathApply(doc_html, '//p', xmlValue))
news_text <- gsub('\\n', ' ', news_text)
news_text <- paste(news_text, collapse = ' ')

head(news_text)

#### If looking to parse a selected URL (e.g. this one from QZ) and run through the same as above
doc_html <- htmlTreeParse("http://qz.com/762729/poor-data-is-hurting-african-countries-ability-to-make-good-policy-decisions/",
                             useInternal = TRUE)
news_text <- unlist(xpathApply(doc_html, '//p', xmlValue))
news_text <- gsub('\\n', ' ', news_text)
news_text <- paste(news_text, collapse = ' ')
