import io
import json


'''
def expandQuery(query,collection,flagArray):
    

    if(collection == 0):
        with io.open('thesaurusCourses.json',encoding='utf8') as f:  
            data = json.load(f) 
    else:
        with io.open('thesaurusReuters.json',encoding='utf8') as f:  
            data = json.load(f) 

    tokenList = query.split()
    string = ''
    for token in tokenList: 
        if(not(token == '') or not(token== ' ')):
            string = string + ' ' +token 
            for indice in data['indexes']:
                if(indice['index'] == token):
                    #print("entre")
                    aux = indice['similarity']
                    print(aux)
                    print(len(aux))
                    if(len(aux) > 0):
                        flagArray[0] = 1
                    for term in aux:
                        string = string + ' ' + term[0]

    return string                
'''        
       
complete_json =  '/Users/Qasim/Desktop/Dev/WebDev/Projects /Js Python/Python-Search-Enigne-IR/Model/Json_data/test_corpus.json'
with open(complete_json, encoding='utf8') as corpus:
            document_filenames = json.load(corpus)    



dataset = {}
dataset['indexes'] = []

def createThesaurus():

    dataset = {}
    dataset['indexes'] = []


    for id in document_filenames:
        docIDs1 = set()
        documents1 = id['description']
        documents1 = id['description']


    terms = wt(id['description'])
    terms = terms + (wt(id['title']))
    #terms = ps(terms)
    unique_terms = set(terms)
    dictionary = dictionary.union(unique_terms)
    for term in unique_terms:
        postings[term][id['doc_id']] = terms.count(term)


    
    
    for i_indice in data['indexes']:
        docIDs1 = set()
        documents1 = i_indice['documents']
        word1= i_indice['index']
        for doc1 in documents1:
            docIDs1.add(doc1[0])
        #only 
        if(len(docIDs1) > 3):
            similarities = []
            for k_indice in data['indexes']:
                docIDs2 = set()
                word2 = k_indice['index']
                if(word1 != word2):
                    documents2 = k_indice['documents']
                    for doc2 in documents2:
                        docIDs2.add(doc2[0])
                    if(len(docIDs2) > 3):
                        ANB = docIDs1 & docIDs2
                        AUB = docIDs1 | docIDs2
                        jaccard = len(ANB) / len(AUB) 
                        if(jaccard > 0.5):
                            aux=[]
                            aux.append(word2)
                            aux.append(jaccard)
                            similarities.append(aux)
            
            if(len(similarities)>0):
                dataset['indexes'].append({
                    'index': word1,
                    'similarity': similarities
                    })

    with open('thesaurusCourses.json', 'w',encoding='utf8') as outfile:  
        json.dump(dataset, outfile, ensure_ascii=False)

createThesaurus()



               
                
        

        

    