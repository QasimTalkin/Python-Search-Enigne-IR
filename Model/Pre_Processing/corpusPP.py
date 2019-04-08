from abc import ABC, abstractmethod
from collections import namedtuple

# Abstract Base Classes (ABCs). 
# Both our corpus will override corpus_preprocess abstract method
#we will use namedtuple() Factory Function for Tuples with Named Fields
#Named tuples assign meaning to each position in a tuple and allow
#for more readable, self-documenting code. They can be used wherever 
#regular tuples are used, and they add the ability to access fields by name instead 
#of position index.
#Documents.namedtuple(typename, field_names, *, rename=False, defaults=None, module=None)

class CorpusPP(ABC):
    def __init__(self):
        self.Document = namedtuple(
            "Document", "doc_id title description snippet topic")
        self.document_list = []
        super().__init__()
    @abstractmethod
    def corpus_pp(self):
        pass
