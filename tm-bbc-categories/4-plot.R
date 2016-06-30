library(plyr)
library(ggplot2)

col <- c("#4c2b26", "#ff4400", "#d9896c", "#d9c7a3", "#d9ad00", 
         "#454d26", "#55f23d", "#00660e", "#00f2c2", "#00ccff", 
         "#006680", "#2d3959", "#0022ff", "#7989f2", "#868cb3", 
         "#240059", "#9b00a6", "#a6537f", "#e5005c", "#8c0013")
  
# read document-topic-matrix and select most likely topic assignment for each article 
docTopic <- read.delim("out/docTopic.csv", sep=",", skip=1, header=F)
smry <- ddply(docTopic, .(V2), summarise, maxProb=max(V4, na.rm=TRUE))
docTopic2 <- merge(docTopic, smry, by.x="V4", by.y="maxProb", all.x=FALSE, all.y=FALSE)

# read topic-word-matrix
topicWords <- read.delim("out/wordTopic.string", sep="\t", header=F)

df <- merge(docTopic2, topicWords, by.x="V3", by.y="V1")
levels(df$V2) <- gsub(",", "\n",levels(df$V2))
df$topic <- paste("topic #",df$V3+1,"\n\n",df$V2, sep="")

# subset to have an even category distribution
samplesize = min(summary(df$V1))

dfsub <- df[1,]
for(l in levels(df$V1)){
  #print( paste(l, dim(df[df$V1==l,])[1], sep=": "))
  part <- df[df$V1==l,]
  sampl <- part[sample(seq(1,dim(part)[1]), samplesize),]
  dfsub <- rbind.data.frame(dfsub, sampl)
}

print(table(dfsub$V1, dfsub$V3))

ggplot(dfsub, aes(topic, fill=as.factor(V1))) + 
  geom_bar(width=0.7) + 
  scale_fill_manual(values=col) +
  theme_bw() + 
  theme(panel.border=element_rect(colour=NA),
        legend.key = element_rect(colour = NA)) +
  labs(x="", fill="",y="number of articles")
