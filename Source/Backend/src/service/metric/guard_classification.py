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

    def predict_metric( self ) -> dict:
        tp, fp, fn, tn = 0, 0, 0, 0
        for idx in range( len( self ) ):
            if not self.judges[ idx ]:
                continue
            label = self.labels[ idx ]
            answer = self.answers[ idx ]

            if label and answer:
                tp += 1
            elif not label and answer:
                fp += 1
            elif label and not answer:
                fn += 1
            elif not label and not answer:
                tn += 1

        total = tp + fp + fn + tn
        accuracy = ( tp + tn ) / ( tp + fp + tn + fn )
        precision = tp / ( tp + fp )
        recall = tp / ( tp + fn )

        return {
            "tp" : tp,
            "fp" : fp,
            "tn" : tn,
            "fn" : fn,
            "total" : total,
            "accuracy" : accuracy,
            "precision" : precision,
            "recall" : recall,
        }