from corpusPP import CorpusPP as cpp
from bs4 import BeautifulSoup as bs4
import requests, json, re, os
from nltk import sent_tokenize 
def tokenize_sentence(text):
    return sent_tokenize(text)

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
            document = self.Document(f'CSI-{docID}', re.sub('\(.*?\)', '', title), description.text.strip() if description is not None else '', snippet, "Uottawa Courses")
            self.document_list.append(document)

        my_dict = [document_list._asdict() for document_list in self.document_list]
        with open ('uottawa_corpus.json', 'w') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=4)
#---------------build--------------------
def setup_uottawa_corpus():
    print("-----Processing Uottawa------")
    uottawaPrep = UottawaPP()
    uottawaPrep.corpus_pp()
    print("------------Done-------------")

setup_uottawa_corpus()

