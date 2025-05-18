from src.interface.evaluation.basic_eval_interface import BasicEvalInterface
from src.interface.llm.basic_llm_interface import BasicLLMInterface

from src.service.benchmark.guard_classification import GuardClassification as GuardCfBm
from src.service.metric.guard_classification import GuardResult
from src.service.llm.basic_llm import default_llm_list


class GuardClassification( BasicEvalInterface ):
    """
    Guard classification evaluation.
    """


    benchmark : GuardCfBm

    bm_size : int
    bm_percentage : float


    def __init__( self, config : dict[ str : str ] ):
        self.benchmark = GuardCfBm()
        self.benchmark.load_data( config[ "file_name" ], config[ "file_type" ] )

        self.bm_size = 100
        self.bm_percentage = 1.0


    def single_evaluate( self, llm : BasicLLMInterface ) -> GuardResult:
        return self.benchmark.run_benchmark( llm, self.bm_size, self.bm_percentage )

    def all_llm_evaluate( self ):
        guard_result_list = []
        for llm in default_llm_list:
            print( llm.single_chat( "whats your name?" ) )
            guard_result_list.append( self.single_evaluate( llm ) )

    def config_benchmark( self, bm_size : int, bm_percentage : float ):
        self.bm_size = bm_size if bm_size is not None else self.bm_size
        self.bm_percentage = bm_percentage if bm_percentage is not None else self.bm_percentage