from abc import ABC, abstractmethod


class BasicResultInterface( ABC ):
    """
    Basic result interface.
    """


    @abstractmethod
    def __len__( self ) -> int:
        pass

    @abstractmethod
    def __getitem__( self, idx : int ) -> dict:
        pass


    @abstractmethod
    def append( self, **kwargs ):
        pass