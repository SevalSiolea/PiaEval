import os
from getpass import getpass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage

from langgraph.graph import START
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatZhipuAI
from langchain_deepseek import ChatDeepSeek

from src.interface.llm.basic_llm_interface import BasicLLMInterface
from src.config import default_config


class BasicLLM( BasicLLMInterface ):
    """
    Basic LLM.
    """


    llm : BaseChatModel

    multi_engine : CompiledStateGraph
    multi_config : dict[ str : dict[ str : str ] ]


    def __init__( self, llm_config : dict[ str : str ] = default_config.default_llm_config() ):
        api_key_name = llm_config[ "api_key_name" ]
        if not os.environ.get( api_key_name ):
            if llm_config[ "api_key" ] != "":
                os.environ[ api_key_name ] = llm_config[ "api_key" ]
            else:
                os.environ[ api_key_name ] = getpass( "Enter { api_key_name }:" )

        if api_key_name == "ZHIPUAI_API_KEY":
            self.llm = ChatZhipuAI( model = llm_config[ "llm_name" ] )
        elif api_key_name == "DEEPSEEK_API_KEY":
            self.llm = ChatDeepSeek( model = llm_config[ "llm_name" ] )
        elif api_key_name == "OPENAI_API_KEY":
            if not os.environ.get( "OPENAI_BASE_URL" ):
                if llm_config[ "OPENAI_BASE_URL" ] != "":
                    os.environ[ "OPENAI_BASE_URL" ] = llm_config[ "base_url" ]
                else:
                    os.environ[ "OPENAI_BASE_URL" ] = getpass( "Enter OPENAI_BASE_URL:" )
            self.llm = ChatOpenAI( model = llm_config[ "llm_name" ] )

        self.launch_multi()


    def single_invoke( self, prompt : str ) -> BaseMessage:
        return self.llm.invoke( prompt )

    def single_chat( self, prompt : str ) -> str:
        return super().single_chat( prompt )

    def multi_invoke( self, prompt : str ) -> BaseMessage:
        if self.multi_engine is None:
            self.launch_multi()

        input_message = { "messages" : [ HumanMessage( prompt ) ] }
        invoke_result = self.multi_engine.invoke( input_message, self.multi_config )
        return invoke_result[ "messages" ][ -1 ]

    def multi_chat( self, prompt : str ) -> str:
        return super().multi_chat( prompt )


    def launch_multi( self ):
        message_state_graph = StateGraph( state_schema = MessagesState )

        message_state_graph.add_edge( START, "model" )
        def call_model( state : MessagesState ) -> dict[ str : BaseMessage ]:
            response = self.llm.invoke( state[ "messages" ] )
            return { "messages" : response }
        message_state_graph.add_node( "model", call_model )

        self.multi_engine = message_state_graph.compile( checkpointer = MemorySaver() )

        self.multi_config = { "configurable" : { "thread_id" : "000000" } }

default_llm_list = [ BasicLLM( llm_config ) for llm_config in default_config.llm_config() ]
default_llm = default_llm_list[ 0 ]