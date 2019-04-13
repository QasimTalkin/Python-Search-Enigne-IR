from corpusPP import CorpusPP as cpp
from bs4 import BeautifulSoup as bs4
import requests, json, re, os
from nltk import sent_tokenize 
from timeit import default_timer as timer

def tokenize_sentence(text):
    return sent_tokenize(text)

topics_json = '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/raw_reut_topics.json'
with open(topics_json) as corpus:
    reut_old_corp = json.load(corpus)


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
        print(f"-----------Reuters PP----------")
        start = timer()
        count = -1
        for files in os.listdir(self.rDataSet):
            with open(os.path.join(self.rDataSet, files), 'rb') as reuterdoc:
                data = reuterdoc.read()
                bs = bs4(data, "html.parser")
#get ones with "reuters" tag
                articles = bs.find_all('reuters')
#Enumerate allows us to loop over something and have an automatic counter.
#docID -> article number starting with 1
#Find title body topic create snippet
                for docID, article in enumerate(articles, 0):

                    count = count+1
                    if count == 19040:
                        count = 899
#Title              
                    title = article.find('title').text if article.find('title') is not None else ""
#Description 
                    description = article.find('body').text if article.find('body') is not None  else ""
#Create Snippet
                    snippet = tokenize_sentence(description.strip())[0] if description is not None and description != "" else ""
#Topic              
                    if (title=="") and (description == "") and (snippet == ""):
                        topic = article.find('topic').text if article.find('topic') is not None  else "Empty Document"
                        count = count - 1
                    else:    
                        topic = article.find('topic').text if article.find('topic') is not None  else reut_old_corp[count]['topics']
#Document
                    document = self.Document(f'{files}-#{docID}', title, description.strip() if description is not None else '', snippet, topic) 
                    self.document_list.append(document)
#Dictionary 
# >>> d = p._asdict()                 # convert to a dictionary
#>>> d['x']
#   11

#Reuters OutPut
        my_dict = [document_list._asdict() for document_list in self.document_list]        
        with open('reuters_corpus.json', 'w', encoding='utf8') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=5)
        end = timer()
        print(f"Reuters PP took {end - start} seconds")
#Uottawa OutPut
        uottawaPrep = UottawaPP()
        self.document_list = self.document_list + uottawaPrep.corpus_pp()
#Complete OutPut
        print(f"-----------Complete PP----------")
        start = timer()
        my_dict = [document_list._asdict() for document_list in self.document_list]        
        with open('complete_corpus.json', 'w', encoding='utf8') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=5)
        end = timer()
        print(f"Complete PP took {end - start} seconds")
#----------------uottawa-----------------

class UottawaPP(cpp):
    def __init__(self):
        super().__init__()
        self.url = 'https://catalogue.uottawa.ca/en/courses/csi/'
        #docID, title, description, snippet
    def corpus_pp(self):
        print(f"-----------Uottawa PP----------")
        start = timer()
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
        with open ('uottawa_corpus.json', 'w', encoding='utf8') as outfile:
            json.dump(my_dict, outfile, ensure_ascii=False, indent=5)
        end = timer()
        print(f"uOttawa PP took {end - start} seconds")
        return self.document_list
#---------------build--------------------
def setup_reuters_corpus():
    print("-----Processing Collection------")
    reutersPrep = ReutersPP()
    reutersPrep.corpus_pp()
    print("------------Done-------------")


#print(reut_old_corp[0]['topics'])
#print(reut_old_corp[889]['topics'])
setup_reuters_corpus()