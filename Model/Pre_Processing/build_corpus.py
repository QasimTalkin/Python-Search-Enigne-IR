from corpusPP import CorpusPP as cpp
from bs4 import BeautifulSoup as bs4
import requests, json, re, os
from nltk import sent_tokenize 
def tokenize_sentence(text):
    return sent_tokenize(text)

class ReutersPP(cpp):
    def __init__(self):
        super().__init__()
        self.rDataSet = os.path.join(os.getcwd(), "dataset")
        #ID, <TITLE>, <BODY>, <TOPICS>

    
#Preprocesses reuters: 
#    * Acessing raw files from the current working directory 
#    * Scraping it using beautiful soup
#    * Storing it in NamedTuples from CorpusPP
#    * Output it in Json 
#    * Creating dictionary list

    def corpus_pp(self):
        for files in os.listdir(self.rDataSet):
            with open(os.path.join(self.rDataSet, files), 'rb') as reuterdoc:
                data = reuterdoc.read()
                bs = bs4(data, "html.parser")
#get ones with "reuters" tag
                articles = bs.find_all('reuters')
#Enumerate allows us to loop over something and have an automatic counter.
#docID -> article number starting with 1
#Find title body topic create snippet
        for docID, article in enumerate(articles, 1):
#Title 
            title = article.find('title').text if article.find('title') is not None else "No Title"
#Description 
            description = article.find('body').text if article.find('body') is not None  else "No Body"
#Topic
            topic = article.find('topic').text if article.find('topic') is not None  else "No Topic"
#Create Snippet
            snippet = tokenize_sentence(description.strip())[0] if description is not None else "No snippet"
#Document
            document = self.Document(f'{files}-article #{docID}', title, description.strip() if description is not None else 'No Description', snippet, topic) 
            self.document_list.append(document)
#Dictionary 
# >>> d = p._asdict()                 # convert to a dictionary
#    >>> d['x']
#   11

        my_dict = [document_list._asdict() for document_list in self.document_list]        


        with open('reuters_corpus.json', 'w') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=5)

def setupcorpus():
    print("-----Processing Reuters------")
    reutersPrep = ReutersPP()
    reutersPrep.corpus_pp()
    print("------------Done-------------")

    print("-----Processing Uottawa------")
    uottawaPrep = UottawaPP()
    uottawaPrep .corpus_pp()
    print("------------Done-------------")

#setupcorpus()