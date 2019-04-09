import re
from collections import defaultdict, Counter
import os
import json

#loading data! 
#complete_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/complete_corpus.json"
complete_json = '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/complete_corpus.json'
with open(complete_json) as corpus:
            DATA = json.load(corpus)



class Search():
    def __init__(self):
        self.index = index_docs(DATA, 'description', 'title', 'doc_id', 'snippet', 'topic')



    def query(self, query, operator='AND', fields=None):
        print('Search for "%s" using %s in %s' % (bold(query), bold(operator), fields or 'all fields'))
        print('-'*80)
        ids = search(self.index, query, operator, fields)
        docID_List = []
        results_count = 0
        for docID, score in ids.most_common():
            document_id = (DATA[docID]['doc_id'])
            #creating result list to acess corpus!
            scorelist = f'{document_id} : {score}'
            docID_List.append(scorelist)
            results_count= results_count + 1

        return docID_List

            
def bold(txt):
    return '\x1b[1m%s\x1b[0m' % txt

SPLIT_RE = re.compile(r'[^a-zA-Z0-9]')
def tokenize(text):
    yield from SPLIT_RE.split(text)

def text_only(tokens):
    for t in tokens:
        if t.isalnum():
            yield t

def lowercase(tokens):
    for t in tokens:
        yield t.lower()

def stem(tokens):
    for t in tokens:
        if t.endswith('ly'):
            t = t[:-2]
        yield t

SYNONYMS = {
    'rapid': 'quick',
}
def synonyms(tokens):
    for t in tokens:
        yield SYNONYMS.get(t, t)

def analyze(text):
    tokens = tokenize(text)
    for token_filter in (text_only, lowercase, stem, synonyms):
        tokens = token_filter(tokens)
    yield from tokens

def index_docs(docs, *fields):
    index = defaultdict(lambda: defaultdict(Counter))
    for id, doc in enumerate(docs):
        for field in fields:
            for token in analyze(doc[field]):
                index[field][token][id] += 1
    return index

def combine_and(*args):
    if not args:
        return Counter()
    out = args[0].copy()
    for c in args[1:]:
        for docID in list(out):
            if docID not in c:
                del out[docID]
            else:
                out[docID] += c[docID]
    return out

def combine_or(*args):
    if not args:
        return Counter()
    out = args[0].copy()
    for c in args[1:]:
        out.update(c)
    return out

COMBINE = {
    'OR': combine_or,
    'AND': combine_and,
}

def search_in_fields(index, query, fields):
    for t in analyze(query):
        yield COMBINE['OR'](*(index[f][t] for f in fields))

def search(index, query, operator='AND', fields=None):
    combine = COMBINE[operator]
    return combine(*(search_in_fields(index, query, fields or index.keys())))




#with open('scores.txt', 'r') as f:
    #index = json.load(f)

#CREATING defaultdict

#with open('scores.txt', 'w') as f:
    #json.dump(index, f)
#search_file = open("search_index.txt","w")
#search_file.write( str(search_index) )
#search_file.close()
#js = open('search_index.json').read()
#index = json.loads(js)



#sample Queries
#result = query(index, 'China India')
#print(f'{result} Results \n')
#query(index, 'China')
#query(index, 'Python')
#query(index, 'Python', fields=['title'])
#query(index, 'python', fields=['description'])
#query(index, 'Python web')
#query(index, 'Python web', 'OR')
#query(index, 'quick')
#query(index, 'rapid')
#query(index, 'of')