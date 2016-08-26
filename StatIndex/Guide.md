# How do you use the Stat Index?       
This tool has been designed for people who are familiar with R but it can be used by anyone with an interest in statistics and news. The Stat Index takes news content, mines the text and measures the use of statistical insights. It was created at BBC News Labs as part of the [Trust Project](http://thetrustproject.org/). The code and statistical dictionary for the project have been made open source. The Stat Index is being updated regularly to include more data and features.

## What is R?
For those unfamiliar with R, it's an extremely popular statistical programming language that's used by Journalists, Researchers and Data Scientists. If you'd like to learn more and download the software, you can do so on the [RStudio site](https://www.rstudio.com/products/rstudio/download2/).

While the Stat Index uses content from an internal BBC tool called Freebird that works with news metadata, it is designed for anyone to use. Feel free to test out your own content by choosing your own URL and running the code in in Part 2.

## The Workflow
After downloading or cloning the repo, there are four parts to the Stat Index.
- Part 1: [JSON](https://github.com/BBC-News-Labs/Text_Analytics/blob/master/StatIndex/StatIndex-Analysis/R%20Code%20-%20StatIndex%20-%20JSON.R) - Take data from Freebird, a tool that stores metadata on news content
- Part 2: [HTML](https://github.com/BBC-News-Labs/Text_Analytics/blob/master/StatIndex/StatIndex-Analysis/R%20Code%20-%20StatIndex%20-%20HTML.R) - Parses HTML from URLs
- Part 3: [Dictionary/Corpus](https://github.com/BBC-News-Labs/Text_Analytics/blob/master/StatIndex/StatIndex-Analysis/R%20Code%20-%20StatIndex%20-%20Dictionary%2C%20Corpus.R) - Build the statistical dictionary and corpus
- Part 4: [Scores](https://github.com/BBC-News-Labs/Text_Analytics/blob/master/StatIndex/StatIndex-Analysis/R%20Code%20-%20StatIndex%20-%20Scoring.R) - Create a series of scores and visualisations.

## Statistical Dictionary
The other element of the Stat Index is the [Statistical Dictionary](https://github.com/BBC-News-Labs/Text_Analytics/tree/master/StatIndex/StatIndex-StatDictionary). This contains a list of statistical terms and data visualisations. Each of these terms has a preliminary complexity score. 

## Contact
If you'd like to get more involved in the development of the Stat Index, please reach out on Github, Twitter or email: <u>liam.bolton@bbc.co.uk</u> 

Please note: the dictionary contains preliminary scores that are in the process of being tested. The dictionary will be updated continuously over the course of the tool’s development.
