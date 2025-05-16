from abc import ABC, abstractmethod

from langchain_core.messages.base import BaseMessage


class BasicLLMInterface( ABC ):
    """
    Basic LLM interface.
    """


    @abstractmethod
    def single_invoke( self, prompt : str ) -> BaseMessage:
        pass

    @abstractmethod
    def single_chat( self, prompt : str ) -> str:
        response = self.single_invoke( prompt )
        return response.content