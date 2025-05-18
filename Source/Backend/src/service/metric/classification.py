from src.interface.metric.basic_result_interface import BasicResultInterface


class GuardResult( BasicResultInterface ):
    """
    Guard result.
    """


    prompts : list[ str ] = []
    labels : list[ bool ] = []
    answers : list[ bool ] = []
    judges : list[ bool ] = []


    def __len__( self ):
        return len( self.prompts )

    def __getitem__( self, idx : int ) -> dict:
        return { "prompt" : self.prompts[ idx ],
            "label" : self.labels[ idx ],
            "answer" : self.answers[ idx ],
            "judge" : self.judges[ idx ]
        }


    def append( self, prompt : str, label : bool, answer : bool, judge : bool ):
        self.prompts.append( prompt )
        self.labels.append( label )
        self.answers.append( answer )
        self.judges.append( judge )