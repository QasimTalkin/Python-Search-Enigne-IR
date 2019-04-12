import io
import json

complete_json =  '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/complete_corpus.json'
with open(complete_json, encoding='utf8') as corpus:
            document_filenames = json.load(corpus)    
topic = set()
for id in document_filenames:
    s = tuple(id['topic'])
    topic.add(s)

print(topic)
topics = str(topic)
with open("Topics_set.txt", "w") as text_file:
    text_file.write(topics)