from abc import ABC, abstractmethod


class Diviner(ABC):
    """
    Base class for study result interpreters.
    
    Diviners serialize study results for API responses.
    Transformation logic has moved to Noctis flows.
    """

    @abstractmethod
    def interpret(self, study_id: int):
        """
        Serialize study results for API response.
        
        Args:
            study_id: Primary key of the study
            
        Returns:
            Serialized study data
        """
        ...