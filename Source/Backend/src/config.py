import os
import json


src_path = os.path.dirname( __file__ )


class Config:
    """
    Config.
    """


    config_path : str
    config : dict = None


    def __init__( self ):
        self.config_path = "config.json"
        self.load_config()


    def load_config( self, path : str = None, encoding : str = "utf-8" ):
        if path is None:
            path = self.config_path
        path = os.path.join( src_path, path )

        with open( path, "r", encoding = encoding ) as config_json:
            self.config = json.load( config_json )

    def llm_config( self ) -> list[ dict[ str : str ] ]:
        if self.config is None:
            self.load_config()

        return self.config[ "llm" ]

    def default_llm_config( self ) -> dict[ str : str ]:
        return self.llm_config()[ 0 ]

    def eval_config( self, task_name : str ) -> list[ dict[ str : str ] ]:
        if self.config is None:
            self.load_config()

        return self.config[ "eval" ][ task_name ]

    def default_eval_config( self, task_name ) -> dict[ str : str ]:
        return self.eval_config( task_name )[ 0 ]


default_config = Config()