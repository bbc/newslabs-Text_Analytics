# Part 4 - Scoring

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
stat_mean <- mean(Terms$frequency)
print(stat_mean)


# Order by frequency of statistical term
order <- Terms[order(Terms$frequency, decreasing=TRUE),]
print(order)


# Merge the dataframe with statistical dictionary to determine complexity of statistical insights used
df_merged <- merge(Terms, dictionary, by="content")


# Remove words in statistical dictionary not used in the news content
df_merged <- df_merged[!apply(df_merged, 1, function(x) {df_merged$frequency == 0}),]


# Explore the data with a quick visualisation of statistical words used in the content
install.packages("ggplot2")
library(ggplot2)

ggplot(df_merged, aes(x=content, y=frequency)) + geom_bar(stat='identity', fill="#99e6ff") + coord_flip()
theme(axis.title=element_blank()) + ggtitle(expression(atop("Frequency of Statistical Insights"))) + 
theme(plot.title = element_text(size=20, hjust=0, color="black"))


# SCORE 4 - Find mean 'complexity' based on a score that measures how advanced the statistical words are
complexity <- mean(df_merged$complexity_prelim, na.rm=TRUE)
print(complexity)


# Merge three of the Stat Index scores into one data frame
scores_merged <- data.frame(sum, complexity, stat_percent)
row.names(scores_merged) <- "Scores"
print(scores_merged)

# Build a table widget showing Stat Index scores, how often it's used in news content and complexity
install.packages("DT")
library(DT)

table_of_scores <- datatable(scores_merged, options = list(pageLength = 5, dom = 'tip'),
    caption = htmltools::tags$caption(
    style = 'caption-side: top; text-align: center;',
    'Stat Index - ', htmltools::em('Total Number of Statistical Insights; Complexity; Percentage Statistics in Content')
  ))

# View table of scores in your browser
table_of_scores

install.packages("htmlWidgets")
library(htmlWidgets)

# Save the table as a widget, potentially embed beneath news content
saveWidget(table_of_scores, file="StatIndexTable.html", selfcontained=TRUE, libdir=NULL)
