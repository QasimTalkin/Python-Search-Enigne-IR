import json
import os
#return document from doc_id
#complete_json = os.path.dirname(os.path.join(os.getcwd()))+"/Json_data/complete_corpus.json"
complete_json = '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/complete_corpus.json'
class CorpusAccess():
    def __init__(self):
        with open(complete_json) as corpus:
            self.corpus = json.load(corpus)

    def access(self, doc_ids):
        for doc in self.corpus:
            if doc['doc_id'] == doc_ids:
                return doc
#Testing 
#example = CorpusAccess()
#output = example.access("CSI-116")
#print("FROM corpus Access", output)

