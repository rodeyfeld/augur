from abc import ABC, abstractmethod

class Diviner(ABC):

    @abstractmethod
    def divine(self, dream):
        ...
    
    @abstractmethod
    def interpret(self, study):
        ...