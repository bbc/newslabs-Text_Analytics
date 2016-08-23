# Part 4 - Scoring based on use of statistical insights in the news content

# SCORE 1 - Total number of statistical words used
sum <- sum(Terms$frequency)
print(sum)

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
write.csv(freqs, "statistical_freqs.csv")

install.packages("d3heatmap")
library(d3heatmap)

Terms$frequency <- rownames(Terms)

# Visualise the frequency of all statistical terms with an interactive D3 heatmap
a <- d3heatmap(Terms, scale="column", dendrogram="none", color="Greens")
a

install.packages("htmlWidgets")
library(htmlWidgets)

# Save the heatmap as a html file
saveWidget(a, file="stat_freq_d3heatmap.html", selfcontained=TRUE, libdir=NULL)

# Use of advanced statistics (complexity) - Scoring needs more research/testing
# Merge the dataframe with statistical dictionary to determine
df_merged <- merge(Terms, dictionary, by="content")
df_merged <- df_merged[1:6]

# Remove words in dictionary not used
df_merged <- df_merged[!apply(df_merged, 1, function(x) {df_merged$frequency == 0}),]

install.packages("ggplot2")
library(ggplot2)

# Visualise statistical words used in content using bar chart
ggplot(df_merged, aes(x=content, y=frequency)) + geom_bar(stat='identity') + coord_flip()
theme(axis.title=element_blank()) + ggtitle(expression(atop("Frequency of Statistical Insights"))) + 
theme(plot.title = element_text(size=20, hjust=0, color="black"))

# SCORE 4 - Find mean 'complexity' based on a score that measures how advanced the statistical words are
complexity <- mean(df_merged$score_3, na.rm=TRUE)
print(complexity)
