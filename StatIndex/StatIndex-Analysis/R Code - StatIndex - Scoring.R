# Part 4 - Scoring based on use of statistics

# SCORE 1 - Total number of statistical words used
sum <- sum(Terms$frequency)
sum

# Create quick if else statement to print statement if news content uses statistical insights or not
if (sum < 1) {
print("This piece of news content does not use statistical words or notation")
} else 
print("This piece of news content uses statistical words or notation")

# Package loads at home, not at BBC. Similar issue when working with local server at BBC
install.packages("qdap")
library(qdap)

# Total number of words in content, Version 1 using qdap
news_word_count <- wc(corpus)

# Total number of words in content, Version 2 (if qdap doesn't load)
corpus_2 <- gsub(' {2,}',' ', news_content)
strsplit(corpus_2,' ')
news_word_count <- length(strsplit(corpus_2,' ')[[1]])
print(news_word_count)

# SCORE 2 - Percentage statistical words in content
stat_percent <- (sum/news_word_count)*100
print(stat_percent)

# SCORE 3 - Mean statistical words based on dictionary dataset
Stat_Score_3 <- mean(Terms$frequency)
print(Stat_Score_3)

# Order by frequency of statistical term
order <- Terms[order(Terms$frequency),]
write.csv(freqs, "C:/Users/boltol02/Projects/statistical_freqs.csv")

install.packages("ggplot2")
library(ggplot2)

# Visualise statistical terms by frequency
ggplot(order, aes(x=content, y=frequency)) + geom_bar(stat='identity') + coord_flip()

# Use of advanced statistics (complexity) - Scoring needs more research/testing
# Merge the dataframe with statistical dictionary to determine
df_merged <- merge(Terms, dictionary, by="content")
df_merged <- df_merged[1:6]

# Remove words in dictionary not used
df_merged <- df_merged[!apply(df_merged, 1, function(x) {df_merged$frequency == 0}),]

# Visualise statistical words used in content
ggplot(df_merged, aes(x=content, y=frequency)) + geom_bar(stat='identity') + coord_flip()

# SCORE 4 - Find mean based on a score that measures how advanced the statistical word is
complexity <- mean(df_merged$score_3, na.rm=TRUE)
print(complexity)

install.packages("DT")
library(DT)

# Create quick table with statistical content
datatable(df_merged, options=list(pageLength=5)


