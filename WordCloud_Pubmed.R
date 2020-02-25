#setwd()
#install.packages("wordcloud")
#install.packages("RColorBrewer")
#install.packages("tm")
library(wordcloud)
library(RColorBrewer)
library(tm)
library(png)
library(dplyr)


abstracts <- read.csv("complete_abstracts.csv")

articles.corpus <- Corpus(VectorSource(abstracts$Abstract))
articles.corpus <- articles.corpus %>% 
                   tm_map(removePunctuation) %>% 
                   tm_map(removeNumbers) %>%
                   tm_map(stripWhitespace)
articles.corpus <- tm_map(articles.corpus, content_transformer(tolower))
articles.corpus <- tm_map(articles.corpus, removeWords, stopwords("english"))

dtm <- TermDocumentMatrix(articles.corpus)
matrix <- as.matrix(dtm)
words <- sort(rowSums(m),decreasing=TRUE)
df <- data.frame(word = names(v),freq=v)

cloud <- wordcloud(words = df$word, freq = df$freq, scale=c(4,0.25), min.freq=2, 
          max.words=100, random.order=T, rot.per=.15, colors=brewer.pal(8, "Dark2"))

#png("wordcloud.png", width=1280,height=800)
#dev.off()
