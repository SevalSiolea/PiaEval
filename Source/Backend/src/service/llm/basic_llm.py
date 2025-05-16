import os
import getpass

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.messages import HumanMessage

from langgraph.graph import START
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from langchain_community.chat_models import ChatZhipuAI

from src.interface.llm.basic_llm_interface import BasicLLMInterface


class BasicLLM( BasicLLMInterface ):
    """
    Basic LLM.
    """


    llm : BaseChatModel

    multi_engine : CompiledStateGraph
    multi_config : dict[ str : dict[ str : str ] ]


    def __init__( self ):
        if not os.environ.get( "ZHIPUAI_API_KEY" ):
            os.environ[ "ZHIPUAI_API_KEY" ] = getpass.getpass( "Enter ZHIPU_API_KEY:" )

        self.llm = ChatZhipuAI( model = "glm-4-flash" )

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