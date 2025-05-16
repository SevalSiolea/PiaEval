import os
import getpass

from langchain_core.language_models import BaseChatModel

from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import BaseMessage

from src.interface.llm.basic_llm_interface import BasicLLMInterface


class BasicLLM( BasicLLMInterface ):
    """
    Basic LLM.
    """


    llm : BaseChatModel


    def __init__( self ):
        if not os.environ.get( "ZHIPUAI_API_KEY" ):
            os.environ[ "ZHIPUAI_API_KEY" ] = getpass.getpass( "Enter ZHIPU_API_KEY:" )

        self.llm = ChatZhipuAI( model = "glm-4-flash" )


    def single_invoke( self, prompt : str ) -> BaseMessage:
        return self.llm.invoke( prompt )

    def single_chat( self, prompt : str ) -> str:
        return super().single_chat( prompt )