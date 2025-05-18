from abc import abstractmethod

from pandas import DataFrame

from src.interface.benchmark.basic_bm_interface import BasicBmInterface

from src.data.benchmark.load_data import load_data


class ClassificationInterface( BasicBmInterface ):
    """
    Classification Benchmark Interface.
    """


    dateset : DataFrame


    @abstractmethod
    def load_data( self, file_name : str, file_type : str ):
        self.dateset = load_data( file_name, "classification", file_type )