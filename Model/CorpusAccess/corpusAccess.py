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
        return [document for document in self.corpus if document['doc_id'] in doc_ids]

#Testing 
#example = CorpusAccess()
#output = example.access("CSI-1")
#print(output)