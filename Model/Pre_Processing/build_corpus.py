from corpusPP import CorpusPP as cpp
from bs4 import BeautifulSoup as bs4
import requests, json, re, os
from nltk import sent_tokenize 
def tokenize_sentence(text):
    return sent_tokenize(text)
#----------------reuters-----------------#
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
            topic = article.find('topic').text if article.find('topic') is not None  else "Reuters Article"
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


#----------------uottawa-----------------

class UottawaPP(cpp):
    def __init__(self):
        super().__init__()
        self.url = 'https://catalogue.uottawa.ca/en/courses/csi/'
        #docID, title, description, snippet
    def corpus_pp(self):
#Preprocesses uottawa: 
#    * scarpinf from https://catalogue.uottawa.ca/en/courses/csi/
#    * Applying beautiful soup
#    * Storing it in NamedTuples from CorpusPP
#    * Output it in Json 
#    * Creating dictionary list
        uottawaCorp = requests.get(self.url)
        bs = bs4(uottawaCorp.text, "html.parser")
        courses = bs.find_all('div', attrs = {'class': 'courseblock'})
#Enumerate allows us to loop over something and have an automatic counter.
#docID -> article number starting with 1
#Find title body topic create snippet
        for docID, course in enumerate(courses, 1):
#Title
            title = course.find('p', attrs = {'class':'courseblocktitle'}).text
#Description
            description = course.find('p', attrs = {'class' :'courseblockdesc'})
#Snippet
            snippet = tokenize_sentence(description.text.strip())[0] if description is not None else ''
#Document 
            document = self.Document(f'CSI={docID}', re.sub('\(.*?\)', '', title), description.text.strip() if description is not None else '', snippet, "Uottawa Courses")
            self.document_list.append(document)

        my_dict = [document_list._asdict() for document_list in self.document_list]
        with open ('uottawa_corpus.json', 'w') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=5)
#---------------build--------------------
def setup_reuters_corpus():
    print("-----Processing Reuters------")
    reutersPrep = ReutersPP()
    reutersPrep.corpus_pp()
    print("------------Done-------------")
def setup_uottawa_corpus():
    print("-----Processing Uottawa------")
    uottawaPrep = UottawaPP()
    uottawaPrep.corpus_pp()
    print("------------Done-------------")
setup_reuters_corpus()
setup_uottawa_corpus()