from abc import ABC, abstractmethod

from src.interface.llm.basic_llm_interface import BasicLLMInterface


class BasicBmInterface(ABC):
    """
    Basic benchmark interface.
    """


    @abstractmethod
    def load_data( self, file_name : str, file_type : str ):
        pass

    @abstractmethod
    def run_benchmark( self, llm : BasicLLMInterface, size : int = 100, percentage : float = 1.0 ):
        pass