from abc import ABC, abstractmethod

from src.interface.benchmark.basic_bm_interface import BasicBmInterface
from src.interface.llm.basic_llm_interface import BasicLLMInterface


class BasicEvalInterface( ABC ):
    """
    Basic evaluation interface.
    """


    benchmark : BasicBmInterface


    @abstractmethod
    def single_evaluate( self, llm : BasicLLMInterface ):
        pass

    @abstractmethod
    def all_llm_evaluate( self ):
        pass

    @abstractmethod
    def config_benchmark( self, **kwargs ):
        pass