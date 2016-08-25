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
order <- Terms[order(Terms$frequency, decreasing=TRUE),]
print(order)


# Merge the dataframe with statistical dictionary to determine complexity of statistical insights used
df_merged <- merge(Terms, dictionary, by="content")
df_merged <- df_merged[1:6]


# Remove words in dictionary not used
df_merged <- df_merged[!apply(df_merged, 1, function(x) {df_merged$frequency == 0}),]

install.packages("ggplot2")
library(ggplot2)

# Explore the data with a quick visualisation of statistical words used in the content
ggplot(df_merged, aes(x=content, y=frequency)) + geom_bar(stat='identity', fill="#99e6ff") + coord_flip()
theme(axis.title=element_blank()) + ggtitle(expression(atop("Frequency of Statistical Insights"))) + 
theme(plot.title = element_text(size=20, hjust=0, color="black"))


# SCORE 4 - Find mean 'complexity' based on a score that measures how advanced the statistical words are
complexity <- mean(df_merged$score_3, na.rm=TRUE)
print(complexity)



# Build a table widget showing statistical term, how often it's used in news content and complexity
install.packages("DT")
library(DT)

# Clean the data - remove and rename columns
df_merged$score <- NULL
df_merged$score_2 <- NULL
colnames(df_merged)[colnames(df_merged) == "score_3"] <- "Complexity"
colnames(df_merged)[colnames(df_merged) == "content"] <- "Term"
colnames(df_merged)[colnames(df_merged) == "frequency"] <- "Count"
df_merged <- df_merged[, c("Term", "Count", "Complexity")]

# Create the data table with statistical terms as the row
a <- datatable(head(df_merged)) %>% 
     formatStyle('Count', 
     background = styleColorBar(df_merged$Count, 'blue'),
     backgroundSize = '100% 90%',
     backgroundRepeat = 'no-repeat',
     backgroundPosition = 'center'
   )
a

install.packages("htmlWidgets")
library(htmlWidgets)

# Save the table as a widget, embed beneath news content
saveWidget(a, file="StatIndexTable.html", selfcontained=TRUE, libdir=NULL)
