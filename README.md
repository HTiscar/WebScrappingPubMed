# WebScrappingPubMed
### A Web Scrapper for abstracts found in PubMed articles.

The basis of this project was my previous attempt for web scrapping, [HTiscar VGChartz Scrapper](https://github.com/HTiscar/WebScrappingVGC).

The main improvements found in this scrapper where the introduction of user inputs, in which you are able to select enabling/disabling the proxies in case you were having problems finding available proxies. 

Additionaly, you are able to access up to two specific keywords necessary for the search of articles in PubMed. May update so you are able to search for unlimited amount of keywords, this time it was just a proof of concept. There is a posibility to find a better solution using the <b>from Browser import Mechanize</b> class. 

### Generating Word Clouds on R

I am adding a visualization element to this code, in the form of <i>wordclouds</i>. The libraries this code uses are <b>wordcloud, tm</b> and <b> RColorBrewer </b>. This is a very basic example of the kind of visualization you can gain from the data generated in the scrapper. Will try to update using the <b>wordcloud2</b> library for better graphics. 

 <p align="center"><img src="https://github.com/HTiscar/WebScrappingPubMed/blob/master/neuronwordcloud.png"></p>
