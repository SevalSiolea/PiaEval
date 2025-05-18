import os

import pandas
import pyarrow

from pandas import DataFrame

from src.config import src_path


def load_data( file_name : str, task_name : str, file_type : str, encoding : str = "utf-8" ) -> DataFrame:
    path = construct_path( file_name, task_name, file_type )
    if file_type == "parquet":
        return load_parquet( path )
    elif file_type == "csv":
        return load_csv( path, encoding )

def load_parquet( path : str ) -> DataFrame:
    return pandas.read_parquet( path, engine = "pyarrow" )

def load_csv( path : str, encoding : str = "utf-8" ) -> DataFrame:
    return pandas.read_csv( path, encoding = encoding )


def construct_path( file_name : str, task_name : str, file_type : str ) -> str:
    file_path = f"{ file_name }.{ file_type }"
    path = os.path.join( src_path, "data", "benchmark", "dataset" )
    path = os.path.join( path, task_name, file_path )
    return path