from abc import ABC, abstractmethod

class Seeker(ABC):

    @abstractmethod
    def seek(self, id) -> "Dream": # type: ignore
        ...
    @abstractmethod
    def poll(self, id) -> "Dream": # type: ignore
        ...
